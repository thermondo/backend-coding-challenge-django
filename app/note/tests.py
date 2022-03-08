from turtle import title
from django.test import TestCase

from .models import Note, Tag
# Create your tests here.

class TagTestCase(TestCase):
    def setUp(self) -> None:
        Tag.objects.create(name="2021")
        Tag.objects.create(name="2022")
        Tag.objects.create(name="news")
    
    def test_tags(self) -> None:
        tag1 = Tag.objects.get(name="2021")
        tag2 = Tag.objects.get(name="2022")
        tag3 = Tag.objects.get(name="news")
        self.assertEqual(tag1.name, "2021")
        self.assertEqual(tag2.name, "2022")
        self.assertEqual(tag3.name, "news")


class NoteTestCase(TestCase):
    def setUp(self) -> None:
        tag1 = Tag.objects.create(name="2021")
        tag2 = Tag.objects.create(name="2022")
        tag3 = Tag.objects.create(name="news")
        note = Note.objects.create(title="Test Note", 
                            body="<h1>Note Body</h1>")
        note.tags.add(tag1, tag3)
    
    def test_tags(self) -> None:
        note = Note.objects.get(id=1)
        tags = []
        for i in note.tags.all():
            tags.append(i.id)
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(tags, [1,3])
