from datetime import datetime
from datetime import timedelta


def now():
    return datetime.utcnow()


def today():
    return now()


def yesterday():
    return today() - timedelta(days=1)


def current_time():
    return now().time()
