from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Note(models.Model):
    author = models.ForeignKey(
        User, related_name="notes", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)
    tags = models.ManyToManyField(
        Tag, related_name="notes")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
