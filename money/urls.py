from django.urls import path

from money.views import (
    home_view,
)

app_name = "money"

urlpatterns = [
    path("", view=home_view, name="home"),
]
