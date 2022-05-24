from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class WorkspaceViewset(viewsets.ModelViewSet):
    queryset = models.Workspace.objects.all()

    def get_queryset(self):
        user = self.request.user
        return models.Workspace.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.WorkspaceDetailSerializer
        return serializers.WorkspaceSerializer

    def get_permissions(self):
        return [IsAuthenticated()]


class TagViewset(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Tag.objects.filter(workspace__owner=user)

    def get_permissions(self):
        return [IsAuthenticated()]


class NoteViewset(viewsets.ModelViewSet):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Note.objects.filter(workspace__owner=user)

    def get_permissions(self):
        return [IsAuthenticated()]
