from datetime import date

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe

from money import models


class DateTimePickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        html += mark_safe(
            """
            <div class="input-group-append">
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
            super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)
        ]
        output.append(
            f'<a href="{self.related_url}" class="btn btn-primary" id="add_id_{name}" onclick="event.preventDefault(); openPopup(this);">Add Another</a>'
        )
        return mark_safe("".join(output))


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


class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = models.TransactionDetail
        exclude = ["transaction"]
        widgets = {
            "item": RelatedFieldWidgetCanAdd(
                models.DetailItem, "money:add_detail_item"
            ),
        }


class DetailItemForm(forms.ModelForm):
    class Meta:
        model = models.DetailItem
        fields = "__all__"
