from django.urls import path

from . import views

app_name = "leetcode"

urlpatterns = [
    path("", view=views.Home.as_view(), name="home"),
]
