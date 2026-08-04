from django.urls import path

from .views import LoginView, UserRegistrationView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
]
