from django.urls import path
from .views import GuestLoginView, LoginView, UserRegistrationView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("guest-login/", GuestLoginView.as_view(), name="guest-login"),
]
