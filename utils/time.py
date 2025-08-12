from datetime import date, datetime, timedelta, timezone

import pytz

TIMEZONE = pytz.timezone("Europe/Moscow")

START_DISCOUNT = timedelta(hours=16, minutes=30)


def get_local_time() -> datetime:
    """Возвращает текущее время в установленном часовом поясу"""
    return datetime.now(TIMEZONE)


def utc_to_local(utc_date: datetime) -> datetime:
    """Принимает UTC дату и возвращает дату в установленном часовом поясе"""
    return pytz.utc.localize(utc_date).astimezone(TIMEZONE)


def get_today_date() -> datetime:
    today = date.today()
    midnight = datetime(
        today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc
    )
    return midnight


def get_last_discount_date() -> datetime:
    """Возвращает дату и время начала прошлого/текущего discount time в deepseek api"""
    now_date = datetime.now(tz=timezone.utc)
    today_date = get_today_date()

    today_start_discount = today_date + START_DISCOUNT
    if now_date <= today_start_discount:
        return today_start_discount - timedelta(days=1)
    else:
        return today_start_discount
