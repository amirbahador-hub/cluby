from django.db.models import QuerySet, Count

from core.models import Benefit, Venue
from core.utils import n_days_ago


def popular_benefits(*, venue:Venue, limit:int = 3, since:int = 180) -> QuerySet[Venue]:
    #query = Benefit.objects.filter(venueid= venue)
    query = venue.benefit_set.all()

    #query = venue.benefit_set.all().annotate(usageCount=Count("benefitusage"))
    return query[:limit]

def popular_benefits(*, limit:int = 3, since:int = 180) -> QuerySet[Venue]:
        query = Venue.objects.prefetch_related(
                Prefetch('benefit_set',
                         queryset=Benefit.objects.annotate(
                             usageCount=Count("benefitusage", filter=Q(benefitusage__usagetimestamp__lt=now()-timedelta(days=180))),
                             ).order_by("-usageCount")
                         ),
                ).all()
 
