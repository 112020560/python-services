from datetime import datetime

from dateutil import tz


def utc_now():
    return datetime.now(tz=tz.UTC)
