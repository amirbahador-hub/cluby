from django.db.models import QuerySet, Prefetch
from datetime import datetime

from core.models import Benefit, BenefitUsage
from core.utils import transition_table
from django.utils import timezone


def available_benefits(
    *, person_id: int, venue_id: int, timestamp: datetime
) -> QuerySet[Benefit]:

    benefits = (
        Benefit.objects.filter(venueid=venue_id)
        .prefetch_related(
            Prefetch(
                "benefitusage_set",
                queryset=BenefitUsage.objects.filter(personid=person_id).order_by(
                    "-usagetimestamp"
                ),
            )
        )
        .all()
    )

    valid_benefits = list()
    for benefit in benefits:
        benefitusages = benefit.benefitusage_set.all()
        if benefitusages.count():
            latest_usage = benefitusages[0].usagetimestamp
            _, checker, days = transition_table[benefit.recurrence][0]
            expire_time = checker(additional_days=days, timestamp=latest_usage)
            if timestamp.astimezone(timezone.utc).replace(tzinfo=None) < expire_time:
                continue
        valid_benefits.append(benefit.id)
    return Benefit.objects.filter(id__in=valid_benefits)
