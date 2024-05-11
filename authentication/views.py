from django.conf import settings
from django.contrib.messages import success as success_msg
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.views import APIView


from ai_store_back.constants import REFRESH_TOKEN_NAME


from .renderers import UserJSONRenderer
from .serializers import (
    LogoSerializer,
    LoginSerializer,
    RefreshSerializer,
    RegistrationSerializer,
    UserSerializer,
)


# test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', UserSerializer)
# 'method' can be used to customize a single HTTP method of a view
# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
# @swagger_auto_schema(methods=['put', 'post'], request_body=UserSerializer)
class RegistrationCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(security=[])
    def post(self, request: Request) -> Response:
        """Create user (without cookie)"""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = serializer.data["username"]
        success_msg(request, f"Создан аккаунт {username}!")

        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(security=[])
    def post(self, request: Request) -> Response:
        """Login (without cookie)"""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


# rf_yasg lib is capable of automatically processing individual HTTP methods of RetrieveUpdateAPIView
@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Get current user", responses={403: "Forbidden"}
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Patch user", responses={403: "Forbidden"}
    ),
)
# The HTTP PUT method is available to call.
# But since it requires providing user information,
# it does not allow you to create users and only allows you to update the user.
# Therefore, the PUT method is meaningless and should be hidden in the API documentation.
@method_decorator(name="put", decorator=swagger_auto_schema(auto_schema=None))
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(request.user)

        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs) -> Response:
        serializer_data = request.data.get("user", {})

        serializer = self.serializer_class(
            instance=request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class RefreshAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshSerializer

    def post(self, request: Request) -> Response:
        """Resfresh token (without cookie)"""
        serializer_data = request.data.get("user", {})

        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class CookieRegistrationCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        operation_summary="(Cookie)",
        security=[],
        responses={
            HTTP_201_CREATED: openapi.Schema(
                properties={
                    "email": openapi.Schema(
                        maxLength=255,
                        type=openapi.FORMAT_EMAIL,
                    ),
                    "username": openapi.Schema(
                        maxLength=255,
                        type=openapi.TYPE_STRING,
                    ),
                    "password": openapi.Schema(
                        maxLength=128,
                        minLength=8,
                        read_only=True,
                        type=openapi.TYPE_STRING,
                    ),
                    "token": openapi.Schema(
                        maxLength=255,
                        type=openapi.TYPE_STRING,
                    ),
                    "logo": openapi.Schema(
                        readOnly=True,
                        type=openapi.FORMAT_URI,
                    ),
                },
                required=["email", "username", "password"],
                title="Registration",
                type=openapi.TYPE_OBJECT,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        """Create user (with cookie)"""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        username = data["username"]
        success_msg(request, f"Создан аккаунт {username}!")

        refresh_token = data.pop(REFRESH_TOKEN_NAME)

        response = Response(data, status=HTTP_201_CREATED)

        # TODO: Check: (HTTPS only = True) => (cookie secure = True)
        response.set_signed_cookie(
            REFRESH_TOKEN_NAME,
            refresh_token,
            salt=settings.REFRESH_TOKEN_SALT,
            max_age=settings.RT_MAX_AGE,
            httponly=True,
            samesite=settings.SAMESITE_COOKIE
            # path="api/v1/users/" # TODO: Figure out: how to set up a path
        )

        return response


class CookieLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="(Cookie)",
        security=[],
        request_body=LoginSerializer,
        responses={
            HTTP_201_CREATED: openapi.Schema(
                properties={
                    "email": openapi.Schema(maxLength=255, type=openapi.FORMAT_EMAIL),
                    "username": openapi.Schema(maxLength=255, type=openapi.TYPE_STRING),
                    "password": openapi.Schema(
                        maxLength=128,
                        minLength=8,
                        read_only=True,
                        type=openapi.TYPE_STRING,
                    ),
                    "token": openapi.Schema(maxLength=255, type=openapi.TYPE_STRING),
                    "logo": openapi.Schema(readOnly=True, type=openapi.FORMAT_URI),
                },
                required=["email", "username", "password"],
                title="User",
                type=openapi.TYPE_OBJECT,
            )
        },
    )
    def post(self, request: Request) -> Response:
        """Login (with cookie)"""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        refresh_token = data.pop(REFRESH_TOKEN_NAME)

        response = Response(data)

        response.set_signed_cookie(
            REFRESH_TOKEN_NAME,
            refresh_token,
            salt=settings.REFRESH_TOKEN_SALT,
            max_age=settings.RT_MAX_AGE,
            httponly=True,
            samesite=settings.SAMESITE_COOKIE,
        )

        return response


class CookieRefreshAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshSerializer

    @swagger_auto_schema(
        operation_summary="(Cookie)", request_body=RefreshSerializer, security=[]
    )
    def post(self, request: Request) -> Response:
        """Refresh token (with cookie)"""
        refresh_token = request._request.get_signed_cookie(
            REFRESH_TOKEN_NAME,
            default=None,
            salt=settings.REFRESH_TOKEN_SALT,
            max_age=settings.RT_MAX_AGE,
        )

        serializer_data = {"refresh_token": refresh_token}

        serializer = self.serializer_class(data=serializer_data)

        try:
            serializer.is_valid(raise_exception=True)
        except KeyError:
            return Response(
                {"detail": "Authentication error. The cookie cannot be decoded."},
                status=HTTP_403_FORBIDDEN,
            )

        response_data = serializer.data

        refresh_token = response_data.pop(REFRESH_TOKEN_NAME)

        response = Response(response_data)

        response.set_signed_cookie(
            REFRESH_TOKEN_NAME,
            refresh_token,
            salt=settings.REFRESH_TOKEN_SALT,
            max_age=settings.RT_MAX_AGE,
            httponly=True,
            samesite=settings.SAMESITE_COOKIE,
        )

        return response


class LogoAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (UserJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Upload user's logo"""
        serializer = self.serializer_class(
            instance=request.user, data=request.FILES, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Delete user's logo"""
        data = {"logo": None}

        serializer = self.serializer_class(
            instance=request.user, data=data, partial=True
        )
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
