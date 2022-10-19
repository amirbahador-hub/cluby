from django.utils import timezone
from datetime import timedelta


def get_n_days_ago(n: int = 180):
    today = timezone.now().date()
    return today - timedelta(days=n)
