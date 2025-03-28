import json
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe

from money import choices
from money.choices import AccountType, RetailerType, TransactionCategory
from money.models.accounts import Account
from money.models.incomes import Salary
from money.models.shoppings import AmazonOrder, DetailItem, Retailer
from money.models.stocks import Stock, StockTransaction
from money.models.transactions import Transaction, TransactionDetail, TransactionFile


class DateTimePickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = """<div class="input-group">"""
        html += super().render(name, value, attrs=attrs, renderer=renderer)
        html += mark_safe(
            """
                <button type="button" class="btn btn-outline-secondary" id="id_increase_date">
                    Increase Date By One
                </button>
            </div>
            """
        )
        return html


class RelatedFieldWidgetCanAdd(widgets.Select):
    def __init__(self, related_model, related_url=None, *args, **kw):
        super().__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = "admin:%s_%s_add" % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [
            '<div class="input-group">',
            super().render(name, value, *args, **kwargs),
            f'<a href="{self.related_url}" class="btn btn-outline-secondary" id="add_id_{name}"'
            + ' onclick="event.preventDefault(); openPopup(this);">Add Another</a>',
            "</div>",
        ]

        return mark_safe("".join(output))


class DynamicKeyValueJSONWidget(forms.Widget):
    template_name = "widgets/dynamic_key_value_JSON.html"

    def __init__(self, initialize_value=None, *args, **kwargs):
        self.subwidget_key_form = kwargs.pop("subwidget_key_form", forms.TextInput)
        self.subwidget_value_form = kwargs.pop(
            "subwidget_value_form", forms.NumberInput
        )
        self.initialize_value = initialize_value
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context_value = value if value else ("",)

        if value == "null" and self.initialize_value:
            context_value = self.initialize_value

        context = super().get_context(name, context_value, attrs)
        final_attrs = context["widget"]["attrs"]
        id_ = context["widget"]["attrs"].get("id")
        context["widget"]["is_none"] = value is None

        subwidgets = []
        for index, item in enumerate(context["widget"]["value"]):
            widget_attrs = final_attrs.copy()
            if id_:
                widget_attrs["id"] = f"{id_}_{index}"
            widget = (
                self.subwidget_key_form(),
                self.subwidget_value_form(attrs={"step": "any"}),
            )
            widget[0].is_required = self.is_required
            widget[1].is_required = self.is_required
            subwidgets.append(
                (
                    widget[0].get_context(name + "_key", item, widget_attrs)["widget"],
                    widget[1].get_context(name + "_value", item, widget_attrs)[
                        "widget"
                    ],
                )
            )

        context["widget"]["subwidgets"] = subwidgets
        return context

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
            key_list = [value for value in getter(name + "_key")]
            value_list = [float(value) for value in getter(name + "_value")]

            return json.dumps({k: v for k, v in zip(key_list, value_list) if v != 0})
        except AttributeError:
            return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        return False

    def format_value(self, value):
        return value or {}


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "retailer",
            "type",
            "date",
            "amount",
            "is_internal",
            "requires_detail",
            "note",
        ]

        widgets = {
            "retailer": RelatedFieldWidgetCanAdd(Retailer, "money:retailer_create"),
            "date": DateTimePickerWidget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["retailer"].choices = sorted(
            self.fields["retailer"].choices, key=lambda x: x[1].lower()
        )
        self.fields["date"].initial = date.today()

        for field_key, field in self.fields.items():
            if field_key in ("is_internal", "requires_detail"):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("account", css_class="form-group col-md-6 mb-0"),
                Column("retailer", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("type", css_class="form-group col-md-4 mb-0"),
                Column("date", css_class="form-group col-md-4 mb-0"),
                Column("amount", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("is_internal", css_class="form-group col-md-6 mb-0"),
                Column("requires_detail", css_class="form-group col-md-6 mb-0"),
            ),
            Column("note", css_class="form-group col-md-12"),
            Submit("submit", "Submit"),
        )


class TransactionUpdateForm(TransactionForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "retailer",
            "type",
            "date",
            "amount",
            "is_internal",
            "requires_detail",
            "note",
            "reviewed",
        ]

        widgets = TransactionForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("account", css_class="form-group col-md-6 mb-0"),
                Column("retailer", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("type", css_class="form-group col-md-4 mb-0"),
                Column("date", css_class="form-group col-md-4 mb-0"),
                Column("amount", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("is_internal", css_class="form-group col-md-4 mb-0"),
                Column("requires_detail", css_class="form-group col-md-4 mb-0"),
                Column("reviewed", css_class="form-group col-md-4 mb-0"),
            ),
            Column("note", css_class="form-group col-md-12"),
            Submit("submit", "Submit"),
        )


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        exclude = ["related_transaction", "amount", "balance"]
        widgets = {
            "date": DateTimePickerWidget(attrs={"class": "form-control"}),
            "stock": RelatedFieldWidgetCanAdd(Stock, "money:stock_create"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].choices = [
            (account.pk, str(account))
            for account in Account.objects.filter(type=AccountType.STOCK).order_by(
                "name"
            )
        ]


class TransactionDetailForm(forms.ModelForm):
    category = forms.ChoiceField(
        label="Item Category", choices=choices.DetailItemCategory.choices
    )

    class Meta:
        model = TransactionDetail
        exclude = ["transaction"]
        widgets = {
            "item": RelatedFieldWidgetCanAdd(DetailItem, "money:detail_item_create"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["item"].choices = [
            (x["pk"], x["name"])
            for x in sorted(
                list(
                    DetailItem.objects.filter(
                        category=choices.DetailItemCategory.ETC
                    ).values("pk", "name")
                ),
                key=lambda x: x["name"].lower(),
            )
        ]
        self.fields["category"].choices = sorted(
            self.fields["category"].choices, key=lambda x: x[1].lower()
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("category", css_class="form-group col-md-6 mb-0"),
                Column("item", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("note", css_class="form-group col-md-4 mb-0"),
                Column("amount", css_class="form-group col-md-4 mb-0"),
                Column("count", css_class="form-group col-md-4 mb-0"),
            ),
            Submit("submit", "Submit"),
        )


class DetailItemForm(forms.ModelForm):
    class Meta:
        model = DetailItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = sorted(
            self.fields["category"].choices, key=lambda x: x[1].lower()
        )


class RetailerForm(forms.ModelForm):
    class Meta:
        model = Retailer
        fields = "__all__"


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = "__all__"
        widgets = {
            "pay_detail": DynamicKeyValueJSONWidget(("Regular HRS",)),
            "adjustment_detail": DynamicKeyValueJSONWidget(
                ("401(K)", "Disability ins", "Healthcare FSA deduction")
            ),
            "tax_detail": DynamicKeyValueJSONWidget(
                (
                    "Federal income tax",
                    "Social security tax",
                    "Medicare tax",
                    "WA Cares Fund Ltc Tax",
                )
            ),
            "deduction_detail": DynamicKeyValueJSONWidget(
                (
                    "ESPP",
                    "Legal Plan",
                    "Disability ins",
                    "Dependent life ins",
                    "Ad&d family ins",
                )
            ),
        }

    def is_valid(self) -> bool:
        return super().is_valid()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["transaction"].choices = [
            (transaction.pk, str(transaction))
            for transaction in Transaction.objects.filter(
                type=TransactionCategory.INCOME,
                retailer__type=RetailerType.INCOME,
                retailer__id=37,
            )
            .filter(reviewed=False)
            .order_by("-date")
        ]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("date", css_class="form-group col-md-4 mb-0"),
                Column("gross_pay", css_class="form-group col-md-4 mb-0"),
                Column("total_adjustment", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("total_withheld", css_class="form-group col-md-4 mb-0"),
                Column("total_deduction", css_class="form-group col-md-4 mb-0"),
                Column("net_pay", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("pay_detail", css_class="form-group col-md-6 mb-0"),
                Column("adjustment_detail", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("tax_detail", css_class="form-group col-md-6 mb-0"),
                Column("deduction_detail", css_class="form-group col-md-6 mb-0"),
            ),
            Column("transaction"),
            Submit("submit", "Submit"),
        )


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"


class AmazonOrderForm(forms.ModelForm):
    class Meta:
        model = AmazonOrder
        exclude = ("transaction", "return_transaction")
        widgets = {
            "date": DateTimePickerWidget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = date.today()


class TransactionFileForm(forms.ModelForm):
    class Meta:
        model = TransactionFile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("file", css_class="form-group")),
            Column("date", css_class="form-group"),
            Column("account", css_class="form-group"),
            Column("note", css_class="form-group"),
            Submit("submit", "Submit", css_class="col-12"),
        )
