import pytest

from core.selectors.availables import available_benefits
from datetime import datetime


@pytest.mark.django_db
def test_available_selector(person1, venue1, benefit1):
    a = available_benefits(person_id=person1, venue_id=venue1, timestamp=datetime.now())
    assert a.first() == benefit1
