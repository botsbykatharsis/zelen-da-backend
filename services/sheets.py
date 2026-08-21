import gspread
import pytz

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

from services.telegram import (
    send_order_notification,
    send_user_confirmation,
)


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json",
    scope
)

client = gspread.authorize(creds)

spreadsheet = client.open("ZelenDa")

products_sheet = spreadsheet.worksheet("Products")
users_sheet = spreadsheet.worksheet("Users")
orders_sheet = spreadsheet.worksheet("Orders")


MOSCOW_TZ = pytz.timezone("Europe/Moscow")


def get_moscow_now():
    return datetime.now(MOSCOW_TZ)


def get_moscow_now_string():
    return get_moscow_now().strftime("%Y-%m-%d %H:%M:%S")

def get_products():
    rows = products_sheet.get_all_records()

    products = []

    for row in rows:
        products.append({
            "id": int(row.get("id", 0)),
            "name": row.get("name", ""),
            "price": int(row.get("price", 0) or 0),
            "image": row.get("image", ""),
            "description": row.get("description", ""),
            "is_promo": str(
                row.get("is_promo", "")
            ).lower() in ["true", "1", "yes"]
        })

    return products

def register_user(user):

    user_id = int(user["user_id"])
    chat_id = int(user["chat_id"])
    username = user.get("username") or "unknown"

    rows = users_sheet.get_all_records()

    for sheet_row, row in enumerate(rows, start=2):
        try:
            existing_user_id = int(row.get("user_id", 0))
        except (TypeError, ValueError):
            continue

        if existing_user_id == user_id:

            users_sheet.update_cell(sheet_row, 2, chat_id)

            users_sheet.update_cell(sheet_row, 3, username)

            return {
                "status": "ok",
                "created": False
            }

    users_sheet.append_row([
        user_id,
        chat_id,
        username,
        get_moscow_now_string(),
        ""
    ])

    return {
        "status": "ok",
        "created": True
    }


def get_user_launch_date(user_id):

    rows = users_sheet.get_all_records()

    for row in rows:
        try:
            existing_user_id = int(row.get("user_id", 0))
        except (TypeError, ValueError):
            continue

        if existing_user_id == int(user_id):
            return str(row.get("bot_launch_date", "")).strip()

    return ""


def get_users():
    return users_sheet.get_all_records()


def mark_reminder_sent(sheet_row):

    users_sheet.update_cell(
        sheet_row,
        5,
        get_moscow_now_string()
    )

def has_user_order(user_id):

    rows = orders_sheet.get_all_records()

    for row in rows:
        try:
            order_user_id = int(row.get("user_id", 0))
        except (TypeError, ValueError):
            continue

        if order_user_id == int(user_id):
            return True

    return False


def create_order(order):
    now = get_moscow_now_string()

    products = get_products()

    readable_items = []
    total_price = 0

    for item in order["items"]:
        product = next(
            (
                p for p in products
                if p["id"] == item["id"]
            ),
            None
        )

        if product:
            readable_items.append(
                f"{product['name']} x{item['qty']}"
            )

            total_price += (
                product["price"] * item["qty"]
            )

    items_str = ", ".join(readable_items)

    user_id = order.get("user_id")

    launch_date = get_user_launch_date(user_id)

    if not launch_date:
        launch_date = now

    row = [
        launch_date,
        user_id,
        order.get("username", "unknown"),
        items_str,
        order.get("name", ""),
        order.get("phone", ""),
        total_price,
        now
    ]

    orders_sheet.append_row(row)

    manager_message = f"""
<b>Новый заказ</b>

👤 {order.get("name", "")}
📞 {order.get("phone", "")}
👤 username: @{order.get("username", "unknown")}

🛒 {items_str}

💰 {total_price} ₽
""".strip()

    send_order_notification(manager_message)

    send_user_confirmation(user_id)

    return {
        "status": "ok",
        "total": total_price
    }