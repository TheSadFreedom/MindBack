from typing import Any, Dict, Tuple
from django.db.models import (
    AutoField,
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    DO_NOTHING,
    ForeignKey,
    ImageField,
    Model,
    TextField,
)


from djmoney.models.fields import MoneyField
from PIL.Image import open as image_open

from ai_store_back.constants import (
    DEFAULT_NEURAL_NETWORK_LOGO_PATH,
    NEURAL_NETWORK_LOGO_UPLOAD_TO_PATH,
)
from authentication.models import User


class NeuralNetwork(Model):
    id = AutoField(primary_key=True)

    name = CharField(max_length=255)

    summary = CharField(max_length=512, default="")

    desc = TextField(default="")

    instruction = TextField(default="")

    logo = ImageField(
        default=DEFAULT_NEURAL_NETWORK_LOGO_PATH,
        upload_to=NEURAL_NETWORK_LOGO_UPLOAD_TO_PATH,
    )

    is_hidden = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)

    updated_at = DateTimeField(auto_now=True)

    author = ForeignKey(User, on_delete=DO_NOTHING)

    def save(self, *args, **kwargs):
        super(NeuralNetwork, self).save(*args, **kwargs)

        logo = image_open(self.logo.path)

        if logo.height > 300 or logo.width > 300:
            output_size = (300, 300)
            logo.thumbnail(output_size)
            logo.save(self.logo.path)

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> Tuple[int, Dict[str, int]]:
        self._delete_last_not_default_logo()
        return super().delete(using, keep_parents)

    def set_logo(self, logo):
        print(type(logo))
        if not logo:
            logo = DEFAULT_NEURAL_NETWORK_LOGO_PATH

        self._set_logo(logo)

    def _set_logo(self, logo):
        print(type(logo))
        self._delete_last_not_default_logo()
        self.image = logo
        self.save()

    def _delete_last_not_default_logo(self):
        if not (self.logo.path == DEFAULT_NEURAL_NETWORK_LOGO_PATH):
            self.logo.delete(save=False)

    def __str__(self) -> str:
        return self.name


class NNMarketData(Model):
    price = MoneyField(
        max_digits=14, decimal_places=2, null=True, default_currency="RUB"
    )

    created_at = DateTimeField(auto_now_add=True)

    neural_network = ForeignKey(NeuralNetwork, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.neural_network}: {self.price} - {self.created_at}"
