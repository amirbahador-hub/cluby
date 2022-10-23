import pytest

from core.selectors.inactives import benefits_inactivity_periods


@pytest.mark.django_db
def test_inactive_selector(person1, venue1, benefit1, benefitusage1):
    data =  benefits_inactivity_periods(venue_id=venue1, since=180)[0]
    
    assert data.get("benefitId") == benefit1.id
