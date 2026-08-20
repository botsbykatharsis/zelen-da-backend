import gspread
from oauth2client.service_account import ServiceAccountCredentials
from services.telegram import send_order_notification, send_user_confirmation
from datetime import datetime
import pytz

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("ZelenDa")

products_sheet = spreadsheet.worksheet("Products")
orders_sheet = spreadsheet.worksheet("Orders")

def get_products():
    rows = products_sheet.get_all_records()

    products = []
    for row in rows:
        products.append({
            "id": int(row.get("id", 0)),
            "name": row.get("name", ""),
            "price": int(row.get("price", 0)),
            "image": row.get("image", ""),
            "description": row.get("description", ""),
            "is_promo": str(row.get("is_promo", "")).lower() in ["true", "1", "yes"]
        })

    return products

def create_order(order):
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    products = get_products()

    readable_items = []
    total_price = 0  # 👈 добавили

    for item in order["items"]:
        product = next((p for p in products if p["id"] == item["id"]), None)
        if product:
            readable_items.append(f"{product['name']} x{item['qty']}")
            total_price += product["price"] * item["qty"]

    items_str = ", ".join(readable_items)

    row = [
        now,
        order.get("username", "unknown"),
        items_str,
        order.get("name", ""),
        order.get("phone", ""),
        total_price,
        now
    ]

    orders_sheet.append_row(row)

    message = f"""
    <b>Новый заказ</b>

    👤 {order.get("name")}
    📞 {order.get("phone")}
    👤 username: @{order.get("username")}

    🛒 {items_str}

    💰 {total_price} ₽
    """

    send_order_notification(message)
    send_user_confirmation(order.get("user_id"))

    return {"status": "ok", "total": total_price}

