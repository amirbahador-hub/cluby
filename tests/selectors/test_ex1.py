import pytest
from core.models import Benefit
from django.test import Client
from django.urls import reverse
from django.conf import settings
from tests.factories import (
        BenefitFactory,
        VenueFactory,
        BenefitUsageFactory,
        PersonFactory,
        )
#from config.settings import base as settings

#from rest_framework.reverse import reverse

#@pytest.fixture()
#def django_db_setup():
#    settings.DATABASES['default'] = {
#        "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "HOST": 'localhost',
#        'ATOMIC_REQUEST': False,
#        "NAME": settings.BASE_DIR / "db.sqlite3",
#            }
#        }

@pytest.mark.django_db
def test_example():
    venue = VenueFactory()
    person = PersonFactory()

    benefit =  BenefitFactory(venueid=venue)
    benefit_usage = BenefitUsageFactory(personid=person, benefitid=benefit)

    client = Client()
    url_ = reverse("core:popular_benefits")
    response = client.get(url_)
    print("hello")
    print(response.content)
    assert 1 == 1
