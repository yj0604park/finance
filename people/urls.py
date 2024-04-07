from django.urls import path

from people import views

app_name = "people"

urlpatterns = [
    path("", view=views.Home.as_view(), name="home"),
]
