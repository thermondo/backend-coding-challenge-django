from dataclasses import fields
from django.test import tag
from rest_framework import serializers

from .models import Tag, Note

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

