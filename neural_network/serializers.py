from rest_framework.validators import UniqueValidator
from rest_framework.serializers import (
    BooleanField,
    CharField,
    HyperlinkedModelSerializer,
    IntegerField,
    ImageField,
)

from authentication.serializers import UserSerializer


from .models import NeuralNetwork


class NeuralNetworkSerializer(HyperlinkedModelSerializer):
    id = IntegerField(read_only=True)

    name = CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=NeuralNetwork.objects.all())],
    )

    summary = CharField(allow_blank=True, max_length=512, required=False)

    desc = CharField(allow_blank=True, required=False)

    instruction = CharField(allow_blank=True, required=False)

    logo = ImageField(required=False)

    is_hidden = BooleanField(required=False)

    author = UserSerializer(allow_null=True, required=False)

    class Meta:
        model = NeuralNetwork
        fields = (
            "id",
            "name",
            "summary",
            "desc",
            "instruction",
            "logo",
            "is_hidden",
            "author",
        )
