import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# =========================
# Подключение к Google Sheets
# =========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# таблица
spreadsheet = client.open("ZelenDa")

# листы
products_sheet = spreadsheet.worksheet("Products")
orders_sheet = spreadsheet.worksheet("Orders")


# =========================
# Получение товаров
# =========================

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


# =========================
# Создание заказа
# =========================

def create_order(order):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # получаем товары (чтобы собрать названия)
    products = get_products()

    readable_items = []
    for item in order["items"]:
        product = next((p for p in products if p["id"] == item["id"]), None)
        if product:
            readable_items.append(f"{product['name']} x{item['qty']}")

    items_str = ", ".join(readable_items)

    row = [
        now,
        order.get("username", "unknown"),
        items_str,
        order.get("name", ""),
        order.get("phone", ""),
        now
    ]

    orders_sheet.append_row(row)

    return {"status": "ok"}