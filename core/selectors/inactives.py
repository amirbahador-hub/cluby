from django.db.models import Prefetch

from core.models import Benefit, BenefitUsage
from core import utils 
from django.db.models import QuerySet, Prefetch
from datetime import datetime, timedelta


def inactivity_periods(duration: int, usage: QuerySet[BenefitUsage]) -> list[dict[str, str] | None]:
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



def benefits_inactivity_periods(*, venue_id: int, since: int = 180) -> list[dict[str, int| dict]]:

    benefits = (
        Benefit.objects.filter(venueid=venue_id)
        .prefetch_related(
            Prefetch(
                "benefitusage_set",
                queryset=BenefitUsage.objects.filter(
                    usagetimestamp__gt=utils.get_n_days_ago(since)
                ).order_by("-usagetimestamp"),
            )
        )
        .all()
    )
    result = list()
    for benefit in benefits:
        _, checker, days = utils.transition_table[benefit.recurrence][1]
        inactive_periods = checker(duration=days, usage=benefit.benefitusage_set.all())
        result.append({"benefitId": benefit.id, "inactivityPeriods": inactive_periods})
    return result


