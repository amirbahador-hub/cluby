import factory

from tests.utils import faker
from core.models import (
        Benefit,
        BenefitUsage,
        Venue,
        Person,
)


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue

    name = factory.LazyAttribute(lambda _: f'django')


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = factory.LazyAttribute(lambda _: f'faker.neme()')


class BenefitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Benefit

    title      = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    recurrence = factory.LazyAttribute(lambda _: f'week')
    venueid    = factory.SubFactory(VenueFactory)


class BenefitUsageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BenefitUsage

    benefitid       = factory.SubFactory(BenefitFactory)
    personid        = factory.SubFactory(PersonFactory)
    usagetimestamp  = factory.LazyAttribute(lambda _: faker.past_date())

