from django.urls import path

from registration.api import LoginView

urlpatterns = [
    path(r'api/v1/auth/login/', LoginView.as_view()),
]
