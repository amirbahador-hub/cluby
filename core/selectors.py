from django.db.models import QuerySet, Count, Q, Prefetch
from datetime import datetime

from core.models import Benefit, Venue, BenefitUsage
from core.utils import get_n_days_ago, transition_table
from django.utils import timezone


def popular_benefits(*, since: int = 180) -> QuerySet[Venue]:
    return Venue.objects.prefetch_related(
        Prefetch(
            "benefit_set",
            queryset=Benefit.objects.annotate(
                usageCount=Count(
                    "benefitusage",
                    filter=Q(benefitusage__usagetimestamp__gt=get_n_days_ago(since)),
                ),
            ).order_by("-usageCount"),
        )
    ).all()


def benefits_inactivity_periods(*, venue_id: int, since: int = 180):

    benefits = (
        Benefit.objects.filter(venueid=venue_id)
        .prefetch_related(
            Prefetch(
                "benefitusage_set",
                queryset=BenefitUsage.objects.filter(
                    usagetimestamp__gt=get_n_days_ago(since)
                ).order_by("-usagetimestamp"),
            )
        )
        .all()
    )
    result = list()
    for benefit in benefits:
        _, checker, days = transition_table[benefit.recurrence][1]
        inactive_periods = checker(duration=days, usage=benefit.benefitusage_set.all())
        result.append({"benefitId": benefit.id, "inactivityPeriods": inactive_periods})
    return result


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
