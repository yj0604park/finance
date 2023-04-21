from datetime import date

from django import forms
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
