from datetime import datetime, timedelta

import pytz

from apscheduler.schedulers.background import BackgroundScheduler

from services.sheets import (
    get_users,
    has_user_order,
    mark_reminder_sent,
)

from services.telegram import send_order_reminder


MOSCOW_TZ = pytz.timezone("Europe/Moscow")

REMINDER_AFTER_DAYS = 3


scheduler = BackgroundScheduler(
    timezone="Europe/Moscow"
)


def parse_launch_date(value):
    try:
        dt = datetime.strptime(
            str(value).strip(),
            "%Y-%m-%d %H:%M:%S"
        )

        return MOSCOW_TZ.localize(dt)

    except (ValueError, TypeError):
        return None


def process_reminders():
    print("Проверка напоминаний...")

    users = get_users()

    now = datetime.now(MOSCOW_TZ)

    for sheet_row, user in enumerate(users, start=2):

        user_id = user.get("user_id")
        chat_id = user.get("chat_id")

        reminder_sent = str(
            user.get("reminder_sent", "")
        ).strip()

        launch_date = parse_launch_date(
            user.get("bot_launch_date", "")
        )

        # Нет необходимых данных
        if not user_id or not chat_id or not launch_date:
            continue

        # Напоминание уже отправлялось
        if reminder_sent:
            continue

        # Ещё не прошло три дня
        if now < launch_date + timedelta(
            days=REMINDER_AFTER_DAYS
        ):
            continue

        # Пользователь уже сделал заказ
        if has_user_order(user_id):
            continue

        try:
            success = send_order_reminder(chat_id)

            if success:
                mark_reminder_sent(sheet_row)

                print(
                    f"Напоминание отправлено: "
                    f"user_id={user_id}"
                )

        except Exception as e:
            print(
                f"Ошибка напоминания "
                f"user_id={user_id}: {e}"
            )


def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        process_reminders,
        trigger="interval",
        hours=1,
        id="order_reminder_job",
        replace_existing=True
    )

    scheduler.start()

    print("Reminder scheduler started")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)