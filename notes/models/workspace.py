from django.db import models

from core import settings


class Workspace(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def notes(self):
        from .note import Note
        return Note.objects.filter(workspace=self)

    def tags(self):
        from .tag import Tag
        return Tag.objects.filter(workspace=self)
