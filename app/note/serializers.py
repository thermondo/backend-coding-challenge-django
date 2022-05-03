from note.models import Note, Tag
from rest_framework import serializers, status
from rest_framework.exceptions import APIException


class TagSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "created", "notes", "updated"]


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'tags',
                  "author", "created", "updated"]

    def create(self, validated_data):
        note = Note.objects.create(
            body=validated_data["body"],
            title=validated_data["title"],
            author=validated_data["author"]
        )
        tags = validated_data.pop("tags", [])
        for tag in tags:
            tg, created = Tag.objects.get_or_create(name=tag["name"])
            note.tags.add(tg)
        return note

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.body = validated_data["body"]
        instance.tags.clear()
        tags = validated_data.pop("tags", [])
        for tag in tags:
            tg, created = Tag.objects.get_or_create(name=tag["name"])
            instance.tags.add(tg)
        instance.save()
        return instance
