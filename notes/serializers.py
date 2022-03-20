from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'workspace')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = ('id', 'created', 'modified', 'title', 'tags')


class NoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = ('id', 'created', 'modified', 'workspace', 'title', 'tags', 'content')


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workspace
        fields = ('id', 'name', 'owner')


class WorkspaceDetailSerializer(serializers.ModelSerializer):

    notes = NoteSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = models.Workspace
        fields = ('id', 'name', 'owner', 'notes', 'tags')
