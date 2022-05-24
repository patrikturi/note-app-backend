from django.urls import path

from registration.api import LoginView, LogoutView

urlpatterns = [
    path(r'api/auth/v1/login/', LoginView.as_view()),
    path(r'api/auth/v1/logout/', LogoutView.as_view()),
]
