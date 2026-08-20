import requests

BOT_TOKEN = "ТВОЙ_ТОКЕН"
MANAGER_CHAT_ID = 123456789  # id менеджера

def send_order_notification(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": MANAGER_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)