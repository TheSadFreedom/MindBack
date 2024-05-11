from django.conf import settings
from django.contrib.auth import authenticate

from jwt import decode as jwt_decode

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (
    CharField,
    HyperlinkedModelSerializer,
    ImageField,
    Serializer,
    ValidationError,
)

from .models import User


# TODO: Add ratelimit.decorators everywhere


class RegistrationSerializer(HyperlinkedModelSerializer):
    email = CharField(max_length=255)

    password = CharField(max_length=128, min_length=8, write_only=True)

    token = CharField(max_length=255, read_only=True)

    refresh_token = CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token", "refresh_token", "logo"]

        read_only_fields = ("logo", "token", "refresh_token")

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(Serializer):
    email = CharField(max_length=255)

    username = CharField(max_length=255, read_only=True)

    password = CharField(max_length=128, min_length=8, write_only=True)

    token = CharField(max_length=255, read_only=True)

    refresh_token = CharField(max_length=255, read_only=True)

    logo = ImageField(read_only=True)

    def validate(self, data: dict[str, str]):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise ValidationError("An email address is required to log in.")

        if password is None:
            raise ValidationError("A password is required to log in.")

        user: User = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError("A user with this email and password was not found.")

        if not user.is_active:
            raise ValidationError("This user has been deactivated.")

        return {
            "email": user.email,
            "username": user.username,
            "token": user.token,
            "refresh_token": user.refresh_token,
            "logo": user.logo,
        }


class UserSerializer(HyperlinkedModelSerializer):
    password = CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "logo")

        read_only_fields = ("logo",)
        write_only_fields = ("password",)

    def update(self, instance: User, validated_data: dict) -> User:
        password: str = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


# TODO: Add a blacklist of tokens
class RefreshSerializer(Serializer):
    token = CharField(max_length=255, read_only=True)
    refresh_token = CharField(max_length=255)

    def validate(self, data: dict) -> dict[str, str]:
        refresh_token = data.get("refresh_token")

        try:
            payload = jwt_decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=settings.JWT_ENCRYPTION_ALGORITHM,
            )
        except Exception:
            msg = f"Authentication error. The token cannot be decoded ({refresh_token})"
            raise AuthenticationFailed(msg)

        try:
            user: User = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            msg = "The user corresponding to this token was not found."
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg = "This user has been deactivated."
            raise AuthenticationFailed(msg)

        return {"token": user.token, "refresh_token": user.refresh_token}


class LogoSerializer(Serializer):
    email = CharField(max_length=255, read_only=True)

    username = CharField(max_length=255, read_only=True)

    logo = ImageField()

    class Meta:
        model = User
        fields = ["email", "username", "logo"]

        read_only_fields = ("email", "username")

    def is_valid(self, data: dict) -> dict:
        if len(data) != 1:
            raise Exception({"detail": "Files Error. One file expected."})
        if "logo" not in data.keys():
            raise Exception({"detail": 'Files Error. File with name "logo" not found.'})
        return data

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_logo(validated_data["logo"])
        instance.save()

        return instance
