from django.shortcuts import render
from rest_framework import viewsets, permissions
# Create your views here.

from .models import Tag, Note
from .serializers import TagSerializer, NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
