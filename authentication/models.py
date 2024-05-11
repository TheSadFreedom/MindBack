from asgiref.sync import async_to_sync


from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
)


from ai_store_back.constants import USER_LOGO_UPLOAD_TO_PATH, DEFAULT_USER_LOGO_PATH


from libs.jwt.gen import generate_token
from libs.image.logo import square_crop_logo


sync_square_crop_user_logo = async_to_sync(square_crop_logo)


class UserManager(BaseUserManager):
    """
    Django requires custom users to define their own
    Manager class. Inheriting from BaseUserManager, we get a lot of the
    same code that Django used to create User.
    """

    def create_user(self, username: str, email: str, password=None):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        email = self.normalize_email(email)  # RFC: foo@BAR.com -> foo@bar.com

        user: User = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = CharField(db_index=True, max_length=255, unique=True)

    email = EmailField(db_index=True, unique=True)

    is_active = BooleanField(default=True)

    is_staff = BooleanField(default=False)

    logo = ImageField(
        default=DEFAULT_USER_LOGO_PATH, upload_to=USER_LOGO_UPLOAD_TO_PATH
    )

    created_at = DateTimeField(auto_now_add=True)

    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def refresh_token(self):
        return self._generate_refresh_token()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        sync_square_crop_user_logo(self.logo.path)

    def get_full_name(self):
        """
        This method is required by Django for things like email processing.
        Usually this is the first and last name of the user, but since we do not
        use them, we will return username.
        """

        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like email processing.
        This is usually the username, but since we don't
        use it, we will return username.
        """

        return self.username

    def set_logo(self, logo_path):
        if not logo_path:
            logo_path = DEFAULT_USER_LOGO_PATH

        self._set_logo(logo_path)

    def _set_logo(self, logo_path):
        self._delete_last_not_default_logo()
        self.image = logo_path
        self.save()

    def _delete_last_not_default_logo(self):
        if not (self.logo.path == DEFAULT_USER_LOGO_PATH):
            self.logo.delete(save=False)

    # TODO: The current token implementation is bad:
    # The token is validated, but then the user is searched in the database. Why?
    # Because the id cannot be forged, otherwise the token will become invalid.
    # The point of JWT is just that you can not climb into the database :(
    def _generate_jwt_token(self):
        return generate_token(
            self.pk,
            settings.SECRET_KEY,
            settings.JWT_ENCRYPTION_ALGORITHM,
            settings.JWT_VALIDITY_PERIOD_IN_DAYS,
        )

    def _generate_refresh_token(self):
        return generate_token(
            self.pk,
            settings.SECRET_KEY,
            settings.JWT_ENCRYPTION_ALGORITHM,
            settings.RT_VALIDITY_PERIOD_IN_DAYS,
        )
