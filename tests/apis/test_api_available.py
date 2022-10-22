import pytest
from django.test import Client
from django.urls import reverse
import json
from datetime import datetime, timedelta


@pytest.mark.django_db
def test_available_api(venue1, benefit1, benefitusage1, person1):
    client = Client()
    url_ = reverse("core:avaliable_benefits")
    req_body = { "personId":person1.id, "venueId":venue1.id,
        "timestamp": str(datetime.now() + timedelta(days=50)) }
            
    response = client.post(url_, data=json.dumps(req_body), content_type='application/json')
    data = json.loads(response.content)[0]
    

    assert response.status_code == 200
    assert data.get("id") == benefit1.id
    assert data.get("recurrence") == benefit1.recurrence
    assert data.get("title") == benefit1.title
    assert data.get("venueId") == venue1.id

