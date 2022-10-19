from django.urls import path
from .views.populars import PopularBenefits
from .views.availables import AvailableBenefits
from .views.inactives import BenefitsInactivity

app_name = "core"
urlpatterns = [
    path("popular/", PopularBenefits.as_view(), name="popular_benefits"),
    path("avaliable/", AvailableBenefits.as_view(), name="avaliable_benefits"),
    path("inactivity/", BenefitsInactivity.as_view(), name="inactivity_periods_of_the_benefits"),
]
