# -*- coding: utf-8 -*-

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from accounts.models import (
    User,
    RecoveryToken)

from common.utils import CommonMixin
from accounts.auth import authenticate, create_token
from accounts.permissions import AllowAny, IsAuthenticated
from accounts.serializers import (
    UserSerializer,
    ProfileSerializer,
)


class SignupAPIView(APIView, CommonMixin):
    permission_classes = (AllowAny,)

    def post(self, request):

        data = request.data
        response_data = {}
        response_data["success"] = True

        if not 'email' in data:
            response_data["message"] = _("email is required ")
            response_data["success"] = False
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        existUser = self.getObjectOrNone(User, email=data["email"])

        if existUser is not None:
            response_data["success"] = False
            response_data["message"] = _("Email already in use")
            return Response(data=response_data, status=status.HTTP_206_PARTIAL_CONTENT)

        serializer = UserSerializer(data=data, many=False)

        if not serializer.is_valid():
            response_data["success"] = False
            response_data["message"] = self.returnSerializerErrors(serializer.errors)
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        created_user = serializer.save()
        response_data = ProfileSerializer(created_user, many=False).data

        return Response(data=response_data, status=status.HTTP_201_CREATED)


class SigninAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        data = request.data
        response_data = {}
        response_data["success"] = False

        if not 'email' in data:
            response_data["message"] = _("email is required ")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        if not 'password' in data:
            response_data["message"] = _("password is required ")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=data["email"], password=data["password"])

        if user is None:
            response_data["message"] = _("Invalid user  or wrong credentials")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data["success"] = True
        response_data["token"] = create_token(user)

        return Response(data=response_data, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView, CommonMixin):
    permission_classes = (AllowAny,)

    def post(self, request):

        response_data = {}
        response_data["success"] = False

        if not 'email' in request.data:
            response_data["message"] = _("Email is required")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        verifyUser = self.getObjectOrNone(User, email=request.data.get('email'))

        if verifyUser is None:
            response_data["message"] = _("Current user doesn't exist")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        hasRecoveryToken = self.getObjectOrNone(RecoveryToken, user=verifyUser, expired=False)

        if hasRecoveryToken is not None:
            htmlMail = render_to_string('email/reset_password.html', {
                'link': '{}{}'.format(settings.FRONTEND_PASSWORD_RESET, hasRecoveryToken.key),
                'email': verifyUser.email

            })

            sendmail = self.sendEmail(
                subject="Forgot your password",
                htmlContent=htmlMail,
                sender="no-reply@support.com",
                to=[verifyUser.email]
            )

            response_data["success"] = True
            response_data["message"] = "%s %s" % (
            _("We'll resend instructions to reset your password to email : "), verifyUser.email)

            return Response(data=response_data, status=status.HTTP_200_OK)

        recovertoken = RecoveryToken()
        recovertoken.user = verifyUser
        recovertoken.save()

        htmlMail = render_to_string('email/reset_password.html', {
            'link': '{}{}'.format(settings.FRONTEND_PASSWORD_RESET, recovertoken.key),
            'email': verifyUser.email

        })

        sendmail = self.sendEmail(
            subject="Forgot your password",
            htmlContent=htmlMail,
            sender="no-reply@support.com",
            to=[verifyUser.email]
        )

        response_data["success"] = True
        response_data["message"] = "%s %s" % (
        _("We send instructions to reset your password to email : "), verifyUser.email)

        return Response(data=response_data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView, CommonMixin):
    permission_classes = (AllowAny,)

    def get(self, request):

        response_data = {}

        recoverToken = request.query_params.get('token')

        if recoverToken is None:
            response_data["success"] = False
            response_data["message"] = _("Must send token by queryparam '?token=yourtoken'")

            return Response(status=status.HTTP_400_BAD_REQUEST, data=response_data)

        verifytoken = self.getObjectOrNone(RecoveryToken, key=recoverToken, expired=False)

        if verifytoken is None:
            response_data["success"] = False
            response_data["message"] = _("Token expired or doesn't exists")

            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data["success"] = True
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data
        response_data = {}

        if 'token' not in data:
            response_data["success"] = False
            response_data["message"] = _("token field are required")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        if 'newpassword' not in data:
            response_data["success"] = False
            response_data["message"] = _("newpassword field are required")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        token = self.getObjectOrNone(RecoveryToken, key=data["token"], expired=False)

        if token is None:
            response_data["success"] = False
            response_data["message"] = _("Token doesn't exist or has expired")

            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        token.user.password = data["newpassword"]
        token.user.save()
        token.expired = True
        token.save()
        response_data["success"] = True

        return Response(data=response_data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        response_data = ProfileSerializer(request.user, many=False).data

        return Response(data=response_data, status=status.HTTP_200_OK)
