from dataclasses import fields
from django.test import tag
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Tag, Note

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__' #['id', 'title', 'body', 'tags', 'author']
        read_only_fields = ['author']
