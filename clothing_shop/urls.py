from django.urls import path
from clothing_shop.views import prediction_dashboard

urlpatterns = [
    path("dashboard/", prediction_dashboard, name="prediction_dashboard"),
]
