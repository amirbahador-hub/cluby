import pytest
from django.test import Client
from django.urls import reverse
import json


@pytest.mark.django_db
def test_popular_benefit_api(venue1, benefit1, benefitusage1, person1):
    client = Client()
    url_ = reverse("core:popular_benefits")
    response = client.get(url_)
    data = json.loads(response.content)

    assert data[0].get("venueId") == venue1.id
    assert len(data)== 1
    assert response.status_code == 200
    assert data[0].get("topBenefits180Days")[0].get("benefitId") == benefit1.id

