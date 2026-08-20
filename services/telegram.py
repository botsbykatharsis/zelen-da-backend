import requests

BOT_TOKEN = "8798010802:AAHggqHM7CXrIazFzzDhuCg0kXKkMYu0fpE"
MANAGER_CHAT_ID = 1326854879

def send_order_notification(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": MANAGER_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)