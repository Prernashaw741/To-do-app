from django.urls import path
from .views import loginView, SignUpView, ForgotPasswordView
urlpatterns = [
    path("login/", loginView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("forgotpassword/", ForgotPasswordView.as_view())
]
