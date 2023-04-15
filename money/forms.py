from django import forms

from money import models


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        exclude = ["balance", "reviewed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["use_for"].choices = sorted(
            self.fields["use_for"].choices, key=lambda x: x[1].lower()
        )
