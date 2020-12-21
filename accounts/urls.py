from django.urls import include, re_path as path
# your urls here

from accounts.views import (
    SignupAPIView,
    SigninAPIView,
    ProfileAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

urlpatterns = [
    path('accounts/$', SignupAPIView.as_view()),
    path('accounts/signin$', SigninAPIView.as_view()),
    path('accounts/me$', ProfileAPIView.as_view()),

    path('accounts/password/forgot$', ForgotPasswordAPIView.as_view()),
    path('accounts/password/reset$', ResetPasswordAPIView.as_view()),
]
