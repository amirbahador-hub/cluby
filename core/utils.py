from django.utils import timezone
from django.db.models import QuerySet, Count, Q, Prefetch
from datetime import timedelta, datetime
from django.utils import timezone
from enum import Enum, auto
from core.models import BenefitUsage


class Action(Enum):
    AVAILABILITY = auto()
    INACTIVITY = auto()


class Recurrence(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


def inactivity_periods(duration: int, usage: QuerySet[BenefitUsage]):
    inactive_time = list()
    pointer_time = datetime.now()
    for bu in usage:
        usage_timestamp = bu.usagetimestamp
        if usage_timestamp < pointer_time - timedelta(days=duration):
            inactive_time.append(
                {
                    "startTime": pointer_time.isoformat(" "),
                    "pointer_time": usage_timestamp.isoformat(" "),
                }
            )
        pointer_time = bu.usagetimestamp

    return inactive_time


def expire_benefit_lock(
    additional_days: int, timestamp: datetime = datetime.now()
) -> datetime:
    return timestamp + timedelta(days=additional_days)


transition_table = {
    Recurrence.DAY.value: [
        (Action.AVAILABILITY, expire_benefit_lock, 1),
        (Action.INACTIVITY, inactivity_periods, 14),
    ],
    Recurrence.WEEK.value: [
        (Action.AVAILABILITY, expire_benefit_lock, 7),
        (Action.INACTIVITY, inactivity_periods, 21),
    ],
    Recurrence.MONTH.value: [
        (Action.AVAILABILITY, expire_benefit_lock, 30),
        (Action.INACTIVITY, inactivity_periods, 30),
    ],
}


def get_n_days_ago(n: int = 180):
    today = timezone.now().date()
    return today - timedelta(days=n)
