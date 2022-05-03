from note.permissions import IsAuthorOrReadOnly
from note.models import Note, Tag
from note.serializers import NoteSerializer, TagSerializer
from rest_framework import viewsets, permissions, generics


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all().order_by("-updated")
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all().order_by("-updated")
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
