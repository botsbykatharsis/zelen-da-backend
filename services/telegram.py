import os
import requests


BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")


def send_message(chat_id, text, parse_mode=None):
    if not BOT_TOKEN:
        print("BOT_TOKEN отсутствует")
        return False

    if not chat_id:
        print("chat_id отсутствует")
        return False

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10
        )

        if not response.ok:
            print(
                "Telegram API error:",
                response.status_code,
                response.text
            )

            return False

        return True

    except Exception as e:
        print(
            "Telegram request error:",
            e
        )

        return False


def send_order_notification(text):
    return send_message(
        MANAGER_CHAT_ID,
        text,
        parse_mode="HTML"
    )


def send_user_confirmation(chat_id):
    return send_message(
        chat_id,
        (
            "Спасибо за заказ! 🌱\n"
            "Скоро наш менеджер с Вами свяжется"
        )
    )


def send_order_reminder(chat_id):
    return send_message(
        chat_id,
        (
            "Вы недавно заглядывали в наш магазин 🌱\n\n"
            "Если ещё не успели оформить заказ — "
            "самое время выбрать свежую микрозелень.\n\n"
            "Будем рады Вашему заказу!"
        )
    )