from django import template
from django.conf import settings
from django.middleware import csrf
from django.utils import timezone
from django.core.mail import BadHeaderError, send_mail
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from app.auth_mgmt.models import CustomUser
# from .serializer import UserRegister, LogoutSerializer
from app.auth_mgmt.utlis import verify_account, TokenGenerator, get_user_details
from .serializers import *
from app.auth_mgmt.signals import *
from app.auth_mgmt.tasks import handle_otp_email_task

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomTokenVerifyView(APIView):
    def get(self, request):
        token_cookie = request.COOKIES.get('ACCESS_TOKEN')

        if token_cookie:
            try:
                access_token = AccessToken(token_cookie)
                access_token.verify()
                return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': 'Token is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Token cookie is required.'}, status=status.HTTP_400_BAD_REQUEST)

class UserEmailRegisterViewset(CreateAPIView):
    """
        This class function is to register user through their email
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegister

    # Register the post_save signal handler
    # @receiver(post_save, sender=MyUser)
    # def create_secret_key(sender, instance, created, **kwargs):
    #     if created:
    #         SecretKey.objects.create(user=instance)

class LoginAPIView(GenericAPIView):
    """
        This class is for login and also set the cookies in user browser
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = Response()
            data = serializer.data
            print(f'SERIALIZER; {serializer.data}')
            if data['mfa_enabled']:
                return Response({'message': 'Verify OTP to continue', 'otp':data['otp']}, status.HTTP_200_OK)

           # Calculate expiration for cookies
            now = timezone.now()
            refresh_expiration = now + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            access_expiration = now + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            response.set_cookie(
                'REFRESH_TOKEN',
                data['refresh'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                expires=refresh_expiration,
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
            )

            response.set_cookie(
                'ACCESS_TOKEN',
                data['access'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                expires=access_expiration,
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
            )

            response['X-CSRFToken'] = csrf.get_token(request)
            response.data = {
                'status': 'successful',
                'data': data,
                'message': 'Login successful. Take token from cookies'
            }
            response.status_code = status.HTTP_200_OK
            return response
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtp(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        user = CustomUser.objects.filter(email=email).first()

        if user.otp == otp:
            user.otp = None
            user.save()

            access_token, refresh_token = generate_token(user)

            response = Response(
                {
                    "success": True,
                    "message": "User Logged in successfully",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)

            return response

        return Response(
            {"success": False, "message": "Invalid OTP"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class LogoutView(GenericAPIView):
    """
        This class is for logout user and remove the cookies from their browser
    """

    # permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def get(self, request):
        token_cookie = request.COOKIES.get('ACCESS_TOKEN')

        if token_cookie:
            try:
                access_token = AccessToken(token_cookie)
                access_token.verify()
                response = Response()
                response.delete_cookie(
                    'REFRESH_TOKEN', domain='.localhost.com')
                response.delete_cookie('ACCESS_TOKEN', domain='.localhost.com')

                response.data = {
                    'status': 'Successfull',
                    'message': 'User logged out successfully'
                }
                response.status_code = status.HTTP_200_OK
                return response

                # return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': 'Token is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Token cookie is required.'}, status=status.HTTP_400_BAD_REQUEST)


def reset_password(request):
    """
        This function to send email to reset their password i.e. when they click forgot password and new mail will be sent to user email so that 
        they can set new password for their account.
    """
    email = request.data['email']
    if email:
        try:
            email = request.data['email'].lower()
        except:
            return Response({
                'status': 'failed',
                'message': 'Email is required to request rest_password'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.get(email=email)
        except:
            response = {
                'status': 'failed',
                'message': 'Email not found.'
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
        subject = "Password reset"
        message = ""
        htmltemp = template.loader.get_template(
            'account_password_reset_email.html')
        c = {
            "email": user.email,
            'domain': get_current_site(request),
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        html_content = htmltemp.render(c)
        try:
            send_mail(subject, message, "noreply@gmail.com",
                      [user.email], fail_silently=False, html_message=html_content)
            response = {
                'status': 'successful',
                'message': "Password reset instructions have been sent to the email address entered.",
            }
            return Response(status=status.HTTP_200_OK, data=response)
        except BadHeaderError:
            response = {
                'status': 'failed',
                'message': 'Invalid header found'
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
    return Response({
        'status': 'failed',
        'message': 'Email is required to request rest_password'
    }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(UpdateAPIView):
    """
        This class is responsible for updating new set password set by user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = PasswordResetConfirmSerializer
    token_generator = default_token_generator
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        try:
            data = {}
            data['new_password'] = request.data['new_password']
            # appending uid and token from url query param to data
            data['uid'] = self.request.query_params.get('uid')
            data['token'] = self.request.query_params.get('token')
            serializer = self.serializer_class(data=data, context={
                'request': request, 'view': self.token_generator})
            if serializer.is_valid(raise_exception=True):
                new_password = serializer.data['new_password']
                serializer.user.set_password(new_password)
                if hasattr(serializer.user, "last_login"):
                    serializer.user.last_login = timezone.now()
                serializer.user.save()

                response = {
                    'status': 'successful',
                    'message': 'Password restored successfully!'
                }
                return Response(status=status.HTTP_200_OK, data=response)
        except:
            response = {
                'status': 'failed',
                'message': 'check uid, token and choose strong password.'
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

class ChangePasswordView(UpdateAPIView):
    """
        This class is to change password when the user are login.
    """
    queryset = CustomUser.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = PasswordChangeSerializer
    http_method_names = ['put']

    def get_object(self):
        # user_id = get_user_details(self)
        user_id = 3
        print(user_id)

        # return CustomUser.objects.get(id=self.request.user.id)
        return Response('id=self.request.user.id')
