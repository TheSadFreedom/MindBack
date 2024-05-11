from django.utils.translation import gettext_lazy as _


from django.db.models import (
    CharField,
    DateTimeField,
    DO_NOTHING,
    ForeignKey,
    Model,
    TextChoices,
)


from djmoney.models.fields import MoneyField


from authentication.models import User


class UserTransactions(Model):
    class TransactionType(TextChoices):
        REPLENISHMENT = "REP", _("Replenishment")
        PURCHASE = "PUR", _("Purchase")

    user = ForeignKey(User, on_delete=DO_NOTHING)

    amount = MoneyField(
        max_digits=14, decimal_places=2, null=True, default_currency="RUB"
    )

    transaction_type = CharField(max_length=3, choices=TransactionType.choices)

    created_at = DateTimeField(auto_now_add=True)

    def get_transaction_type_as_enum(self) -> TransactionType:
        return self.TransactionType[self.transaction_type]
