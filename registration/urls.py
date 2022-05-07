from django.urls import path

from registration.api import LoginView, LogoutView

urlpatterns = [
    path(r'api/v1/auth/login/', LoginView.as_view()),
    path(r'api/v1/auth/logout/', LogoutView.as_view()),
]
