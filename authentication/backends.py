from django.conf import settings


from jwt import decode as jwt_decode

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


# from ai_store_back.constants import (
#    SIGNED_HTTP_ONLY_COOKIE_AUTH as COOKIE,
#    ACCESS_TOKEN_NAME,
# )


from .models import User


class JWTAuthentication(BaseAuthentication):
    authentication_header_prefix = "Bearer"
    # API_COOKIE_AUTH = f"/api/{COOKIE}/"

    def authenticate(self, request: Request):
        """
        The authenticate method is called every time, regardless of
        whether the authentication endpoint requires it. 'authenticate' has two possible
        return values:
        1) None - we return None if we don't want to authenticate.
        This usually means that we know that authentication will fail.
        An example of this is, the case when the token is not included in
        the header.
        2) (user, token) - we return the user/token combination
        when authentication is successful. If none of
        the cases are met, it means that an error has occurred and we
        are not returning anything. In this case, we'll just throw an exception
        AuthenticationFailed and let DRF do the rest.
        """
        request.user = None

        # URI (Uniform Resource Identifier) = URL (Locator) + URN (Name)
        # if self.API_COOKIE_AUTH in request.get_full_path():
        #    token = request.get_signed_cookie(
        #        ACCESS_TOKEN_NAME, default=None, salt="", max_age=None
        #    )
        #
        #    if not token:
        #        return None
        # else:

        # 'auth_header' should be an array with two elements:
        # 1) the name of the authentication header (Token in our case)
        # 2) the JWT itself, by which we must authenticate
        auth_header = get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header, one element is passed in the header
            return None

        elif len(auth_header) > 2:
            # Incorrect token header, some extra whitespace characters
            return None

        # JWT library we use usually handles incorrectly
        # bytes type, which is commonly used by standard libraries
        # Python3 (HINT: use PyJWT). To solve this exactly, we need
        # decode prefix and token. It's not the cleanest code, but it's a good one.
        # solution, because a mistake is possible if we don't do it.
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            # The header prefix is not the one we expected - failure.
            return None

        # By now there is a "chance" that authentication will be successful.
        # We delegate the actual authentication of credentials to the method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request: Request, token: str):
        """
        Authentication attempt with the provided data. If successful,
        return the user and the token, otherwise, generate an exception.
        """
        try:
            payload = jwt_decode(
                token, settings.SECRET_KEY, algorithms=settings.JWT_ENCRYPTION_ALGORITHM
            )
        except Exception:
            msg = f"Authentication error. The token cannot be decoded ({token}), [{settings.SECRET_KEY}])"
            raise AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            msg = "The user corresponding to this token was not found."
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg = "This user has been deactivated."
            raise AuthenticationFailed(msg)

        return (user, token)
