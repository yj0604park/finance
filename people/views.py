from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from . import models


# Create your views here.
class Home(LoginRequiredMixin, ListView):
    model = models.Person
    template_name = "people/home.html"
