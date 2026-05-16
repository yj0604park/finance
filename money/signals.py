from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from money.models.accounts import Account
from money.models.transactions import Transaction


@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_account_last_transaction(sender, instance, raw=False, **kwargs):
    if raw or instance.account_id is None:
        return

    last = (
        Transaction.objects.filter(account_id=instance.account_id)
        .order_by("-date", "-id")
        .values_list("date", flat=True)
        .first()
    )
    Account.objects.filter(pk=instance.account_id).update(last_transaction=last)
