from django.contrib import auth
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from app.auth_mgmt.models import CustomUser
from app.auth_mgmt.utlis import validate_password, generate_token

# from app.auth_mgmt.signals import *
from app.auth_mgmt.tasks import handle_otp_email_task


class UserRegister(serializers.ModelSerializer):
    """
    User registration serializer
    """

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2", "recovery_code"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    def save(self, **kwargs):
        user = CustomUser(
            email=self.validated_data["email"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        validate_password(password, password2)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    otp = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    mfa_enabled = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "refresh", "access", "mfa_enabled", "otp"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        try:
            user_data = CustomUser.objects.get(email=email)
        except:
            raise serializers.ValidationError(
                {"status": "failed", "message": "enter valid email"}
            )
        if not user_data.is_active:
            raise AuthenticationFailed(
                {"status": "failed", "message": "Account is not active."}
            )
        if not user:
            raise AuthenticationFailed(
                {"status": "failed", "message": "Invalid credentials, Try Again."}
            )

        refresh_token, access_token = generate_token(user)

        if user_data.mfa_enabled:
            otp = generate_otp()
            handle_otp_email_task.delay(email, otp)  # Celery Task
            # otp_generate.send(sender=None, otp=otp)
            user_data.otp = otp  # Store OTP in user object
            user_data.save()
            return {
                "message": "OTP has been sent",
                "mfa_enabled": user_data.mfa_enabled,
                "email": user.email,
                "otp": otp,
            }
        return {
            "email": user.email,
            "refresh": refresh_token,
            "access": access_token,
            "mfa_enabled": user_data.mfa_enabled,
        }


class PasswordChangeSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )
    re_new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )

    class Meta:
        model = CustomUser
        fields = ["current_password", "new_password", "re_new_password"]

    def validate(self, attrs):
        old_password = attrs.get("current_password")
        self.validate_old_password(old_password)
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = 3
        print(user)
        if user.check_password(value) == False:
            raise serializers.ValidationError(
                {"current_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        new_password = validated_data["new_password"]
        re_new_password = validated_data["re_new_password"]
        validate_password(new_password, re_new_password)
        instance.set_password(new_password)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email"]


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    """
    Serializer for confirming a password reset.

    Validates the 'uid' and 'token' sent by the user, and sets a new password.
    """

    uid = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """

        model = CustomUser
        fields = ["uid", "token", "new_password"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = None  # Initialize user in __init__

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = urlsafe_base64_decode(self.initial_data.get("uid", ""))
            self.user = CustomUser.objects.get(pk=uid)
        except (CustomUser.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise serializers.ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = self.context["view"].check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise serializers.ValidationError({"token": "invalid token"})


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            serializers.ValidationError(
                {"status": "failed", "message": "Bad refresh token"}
            )
