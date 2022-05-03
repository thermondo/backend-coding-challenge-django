from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
import json
from rest_framework.test import force_authenticate
from note.views import NoteList, NoteDetail, NotesTagList


class NoteTestSuit(TestCase):
    payload = {
        "title": "Hey",
        "body": "there",
        "tags": [{"name": "blah"}]
    }
    url = {
        "notes": "/notes/",
        "tags": "/tags/"
    }
    content_type = 'application/json'

    def setUp(self):
        self.factory = APIRequestFactory()
        super_user = {"email": "admin@test.com", "password": "admin@test0"}
        user = {"email": "test@test.com", "password": "test@test1"}
        another_user = {"email": "another.test@test.com",
                        "password": "anothertest@test1"}

        self.super_user = User.objects.create_superuser(
            super_user.get("email"),
            super_user.get("password"))
        self.user = User.objects.create_user(
            user.get("email"),
            user.get("password"))
        self.another_user = User.objects.create_user(
            another_user.get("email"),
            another_user.get("password"))

    def test_unauthorized_add_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        # Bad request
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_add_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_update_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        self.payload["title"] = "heyy"
        pk = response.data.get("id")
        url = "{route}{id}/".format(route=self.url.get("notes"),
                                    id=pk)
        request = self.factory.put(url,
                                   json.dumps(self.payload),
                                   content_type=self.content_type)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.another_user)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 403)

    def test_update_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        self.payload["title"] = "heyy"
        pk = response.data.get("id")
        url = "{route}{id}/".format(route=self.url.get("notes"),
                                    id=pk)
        request = self.factory.put(url,
                                   json.dumps(self.payload),
                                   content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_delete_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        pk = response.data.get("id")
        url = "{route}{id}/".format(route=self.url.get("notes"),
                                    id=pk)
        request = self.factory.delete(url)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.another_user)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 403)

    def test_delete_note(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        pk = response.data.get("id")
        url = "{route}{id}/".format(route=self.url.get("notes"),
                                    id=pk)
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = NoteDetail.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 204)

    def test_list_notes(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        request = self.factory.get(self.url.get("notes"))
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_tags_notes_of_user(self):
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.another_user)
        another_response = NoteList.as_view()(request)

        self.payload["title"] = "heyhey"
        self.payload["tags"] = [{"name": "blahblah"}]
        request = self.factory.post(self.url.get("notes"),
                                    json.dumps(self.payload),
                                    content_type=self.content_type)
        force_authenticate(request, user=self.user)
        response = NoteList.as_view()(request)
        tag = response.data.get("tags")[0]["id"]
        url = "{route}{tag}/notes".format(route=self.url.get("tags"),
                                          tag=tag)
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = NotesTagList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        tag = another_response.data.get("tags")[0]["id"]
        url = "{route}{tag}/notes".format(route=self.url.get("tags"),
                                          tag=tag)
        request = self.factory.get(url)
        force_authenticate(request, user=self.another_user)
        response = NotesTagList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
