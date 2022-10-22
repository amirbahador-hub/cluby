import pytest
from django.test import Client
from django.urls import reverse
import json


@pytest.mark.django_db
def test_empty_periods(venue1, benefit1, benefitusage1, person1):
    client = Client()
    url_ = reverse("core:inactivity_periods_of_the_benefits")
    response = client.get(url_)
    data = json.loads(response.content)

    assert data == list()
    assert response.status_code == 200

