from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from money.models.accounts import Bank

from .serializers import BankSerializer


class BankViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
