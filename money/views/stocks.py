from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from money.forms import StockForm
from money.models.stocks import Stock


class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = "stock/stock_detail.html"


stock_detail_view = StockDetailView.as_view()


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock/stock_create.html"


stock_create_view = StockCreateView.as_view()
