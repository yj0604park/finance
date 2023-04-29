import json
from datetime import date

from django import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from money import models


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
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

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
            super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs),
            f'<a href="{self.related_url}" class="btn btn-outline-secondary" id="add_id_{name}" onclick="event.preventDefault(); openPopup(this);">Add Another</a>',
            "</div>",
        ]

        return mark_safe("".join(output))


class KeyValueJSONWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput, forms.TextInput]
        super().__init__(widgets, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = [super().render(name, value, attrs=attrs, renderer=renderer)]

        output.append('<button type="button" id="add-keyvalue">Add</button>')
        return mark_safe("".join(output))

    def decompress(self, value):
        if value and value != "null":
            return [value, None]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)

        return json.dumps(value)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = [
            "account",
            "retailer",
            "type",
            "datetime",
            "amount",
            "is_internal",
            "requires_detail",
            "note",
        ]

        widgets = {
            "retailer": RelatedFieldWidgetCanAdd(
                models.Retailer, "money:retailer_create"
            ),
            "datetime": DateTimePickerWidget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["retailer"].choices = sorted(
            self.fields["retailer"].choices, key=lambda x: x[1].lower()
        )
        self.fields["datetime"].initial = date.today()

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
                Column("datetime", css_class="form-group col-md-4 mb-0"),
                Column("amount", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("is_internal", css_class="form-group col-md-6 mb-0"),
                Column("requires_detail", css_class="form-group col-md-6 mb-0"),
            ),
            Column("note", css_class="form-group col-md-12"),
            Submit("submit", "Submit"),
        )


class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = models.TransactionDetail
        exclude = ["transaction"]
        widgets = {
            "item": RelatedFieldWidgetCanAdd(
                models.DetailItem, "money:detail_item_create"
            ),
        }


class DetailItemForm(forms.ModelForm):
    class Meta:
        model = models.DetailItem
        fields = "__all__"


class RetailerForm(forms.ModelForm):
    class Meta:
        model = models.Retailer
        fields = "__all__"


class SalaryForm(forms.ModelForm):
    transaction_id = forms.IntegerField()

    class Meta:
        model = models.Salary
        fields = (
            "date",
            "gross_pay",
            "total_adjustment",
            "total_withheld",
            "total_deduction",
        )
        # exclude = ("transaction",)
        # widgets = {"pay_detail": KeyValueJSONWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("date", css_class="form-group col-md-6 mb-0"),
                Column("gross_pay", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("total_adjustment", css_class="form-group col-md-4 mb-0"),
                Column("total_withheld", css_class="form-group col-md-4 mb-0"),
                Column("total_deduction", css_class="form-group col-md-4 mb-0"),
            ),
            Submit("submit", "Submit"),
        )
