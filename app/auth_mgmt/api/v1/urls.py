from django.urls import path, include
from .views import *
from rest_framework import routers
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
router = routers.DefaultRouter()
# router.register(r'verify-otp', VerifyOtp, basename='VerifyOtp')
app_name = "auth_app"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/reset/", reset_password, name="reset-password"),
    path(
        "password/reset/confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("register/", UserEmailRegisterViewset.as_view(), name="user-register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("verify-otp/", VerifyOtp.as_view(), name="verify-otp"),
]
