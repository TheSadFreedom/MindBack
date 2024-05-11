from django.urls import include, path


from .views import (
    LogoAPIView,
    CookieLoginAPIView,
    CookieRefreshAPIView,
    CookieRegistrationCreateAPIView,
    LoginAPIView,
    RefreshAPIView,
    RegistrationCreateAPIView,
    UserRetrieveUpdateAPIView,
)


app_name = "authentication"

patterns_v0 = [
    path("user/", UserRetrieveUpdateAPIView.as_view()),
    path("users/", RegistrationCreateAPIView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
    path("users/refresh/", RefreshAPIView.as_view()),
]

patterns_v1 = [
    path("user/", UserRetrieveUpdateAPIView.as_view()),
    path("user/logo/", LogoAPIView.as_view()),
    path("users/", CookieRegistrationCreateAPIView.as_view()),
    path("users/login/", CookieLoginAPIView.as_view()),
    path("users/refresh/", CookieRefreshAPIView.as_view()),
]

urlpatterns = [path("", include(patterns_v0)), path("v1/", include(patterns_v1))]
