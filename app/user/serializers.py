from django.contrib.auth.models import User, Group
from rest_framework import serializers
from note.models import Note


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', "notes"]
