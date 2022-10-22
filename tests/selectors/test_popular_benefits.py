import pytest

from core.models import Benefit
from core.selectors import popular_benefits

from django.test import Client
from django.urls import reverse
from django.conf import settings

from tests.factories import (
        BenefitFactory,
        VenueFactory,
        BenefitUsageFactory,
        PersonFactory,
        )

@pytest.fixture
def venue1():
    return VenueFactory()


@pytest.fixture
def person1():
    return PersonFactory()


@pytest.fixture
def benefit1(venue1):
    return BenefitFactory(venue=venue1)


@pytest.fixture
def benefitusage1(benefit1, person1):
    return BenefitUsageFactory(benefitid=benefit1, personid=person1)

@pytest.mark.django_db
def test_example(venue1):
    #venue = VenueFactory()
    #person = PersonFactory()

    #benefit =  BenefitFactory(venueid=venue)
    #benefit_usage = BenefitUsageFactory(personid=person, benefitid=benefit)

    #client = Client()
    #url_ = reverse("core:popular_benefits")
    #response = client.get(url_)
    #print("hello")
    #print(response.content)
    #print(popular_benefits())
    assert popular_benefits()[0] == venue1
