from django.db import models

from core import settings


class Workspace(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='workspaces', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
