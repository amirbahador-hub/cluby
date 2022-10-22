import pytest

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
