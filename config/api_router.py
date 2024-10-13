from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from finance.users.api.views import UserViewSet
from money.api.views import BankViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("money", BankViewSet)


app_name = "api"
urlpatterns = router.urls
