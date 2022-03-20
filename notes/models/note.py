from django.db import models
from model_utils.models import TimeStampedModel

from .workspace import Workspace
from .tag import Tag


class Note(TimeStampedModel, models.Model):
    workspace = models.ForeignKey(Workspace, related_name='notes', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
