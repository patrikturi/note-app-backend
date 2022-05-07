from django.urls import path

from django.contrib.auth.views import LoginView

urlpatterns = [
    path(r'login/', LoginView.as_view(template_name='admin/login.html')),
]
