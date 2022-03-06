from django.db import models

from .workspace import Workspace


class Tag(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='tags', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
