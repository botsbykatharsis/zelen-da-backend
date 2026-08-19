import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# подключение
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("ZelenDa").worksheet("Orders")

# временные товары
products_data = [
    {
        "id": 1,
        "name": "Микрозелень горох",
        "price": 150,
        "image": "https://via.placeholder.com/150",
        "description": "Свежая микрозелень гороха",
        "is_promo": True
    },
    {
        "id": 2,
        "name": "Микрозелень редис",
        "price": 120,
        "image": "https://via.placeholder.com/150",
        "description": "Острая микрозелень редиса",
        "is_promo": False
    }
]


def get_products():
    return products_data


def create_order(order):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # делаем читаемый список товаров
    readable_items = []
    for item in order["items"]:
        product = next((p for p in products_data if p["id"] == item["id"]), None)
        if product:
            readable_items.append(f"{product['name']} x{item['qty']}")

    items_str = ", ".join(readable_items)

    row = [
        now,
        order.get("username", "unknown"),
        items_str,
        order["name"],
        order["phone"],
        now
    ]

    sheet.append_row(row)

    return {"status": "ok"}