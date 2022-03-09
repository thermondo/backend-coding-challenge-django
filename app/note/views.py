from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
# Create your views here.

from .models import Tag, Note
from .serializers import TagSerializer, NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Note.objects.filter(public=True)
        else:
            return Note.objects.filter(author=self.request.user)


class NoteList(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filterset_fields = ['tags__name']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Note.objects.filter(public=True)
        else:
            return Note.objects.filter(author=self.request.user)


class NoteSearch(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filterset_fields = ['body', 'title']

    def get_queryset(self):
        search = self.request.GET.get('body')
        if search:
            if self.request.user.is_anonymous:
                return Note.objects.filter(body__contains=search, public=True)
            else:
                return Note.objects.filter(body__contains=search, author=self.request.user)
        else:
            if self.request.user.is_anonymous:
                return Note.objects.filter(public=True)
            else:
                return Note.objects.filter(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
