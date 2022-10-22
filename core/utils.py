from django.utils import timezone
from datetime import timedelta, datetime
from django.utils import timezone
from enum import Enum, auto
from core.selectors.inactives import inactivity_periods


class Action(Enum):
    AVAILABILITY = auto()
    INACTIVITY = auto()


class Recurrence(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"



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
