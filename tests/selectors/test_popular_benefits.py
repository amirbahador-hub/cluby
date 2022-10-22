import pytest

from core.selectors.populars import popular_benefits


@pytest.mark.django_db
def test_example(venue1):
    assert popular_benefits().first() == venue1
