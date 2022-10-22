from django.db.models import QuerySet, Count, Q, Prefetch

from core.models import Benefit, Venue
from core.utils import get_n_days_ago


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


