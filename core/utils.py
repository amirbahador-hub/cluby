from django.utils import timezone
from datetime import timedelta, datetime
from django.utils import timezone
from enum import Enum


class Recurrence(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


def get_n_days_ago(n: int = 180):
    today = timezone.now().date()
    return today - timedelta(days=n)


def expire_benefit_lock(
    recurrence: Recurrence, timestamp: datetime = datetime.now()
) -> datetime:
    if recurrence == Recurrence.DAY.value:
        return timestamp + timedelta(days=1)
    elif recurrence == Recurrence.WEEK.value:
        return timestamp + timedelta(days=7)
    elif recurrence == Recurrence.MONTH.value:
        return timestamp + timedelta(days=30)
