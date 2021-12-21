import json

from django.contrib.auth.models import User
from django.db.models.aggregates import Avg, Count
from django.db.models.expressions import Case, When
from django.http import response
from django.test.testcases import SerializeMixin
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializer import BookSerializer


class BookApiTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test_username")
        self.book1 = Book.objects.create(
            name="Test book 1 xere", price=25, author="Author 2", owner=self.user1
        )
        self.book2 = Book.objects.create(
            name="Test book 2", price=55, author="Author 2"
        )
        self.book3 = Book.objects.create(
            name="Test book 3 xere", price=55, author="Author 3"
        )
        UserBookRelation.objects.create(
            user=self.user1, book=self.book1, like=True, rate=4.5
        )

    def test_get(self):
        url = reverse("book-list")
        self.client.force_login(self.user1)
        response = self.client.get(url)
        books = (
            Book.objects.all()
            .annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg("userbookrelation__rate"),
            )
            .order_by("id")
        )
        serializer_data = BookSerializer(books, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]["rating"], "4.00")
        self.assertEqual(serializer_data[0]["annotated_likes"], 1)

    def test_post(self):
        url = reverse("book-list")
        data = {
            "name": "Programming in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user1, Book.objects.last().owner)

    def test_put(self):
        url = reverse("book-detail", args=(self.book1.id,))
        data = {"name": self.book1.name, "price": 75, "author_name": self.book1.author}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(75, self.book1.price)

    def test_put_not_owner(self):
        self.user1 = User.objects.create(username="test_username2")
        url = reverse("book-detail", args=(self.book1.id,))
        data = {"name": self.book1.name, "price": 75, "author_name": self.book1.author}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(55, self.book2.price)

    def test_put_not_owner_but_staff(self):
        self.user1 = User.objects.create(username="test_username2", is_staff=True)
        url = reverse("book-detail", args=(self.book1.id,))
        data = {"name": self.book1.name, "price": 75, "author_name": self.book1.author}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.book1.refresh_from_db()
        self.assertEqual(55, self.book2.price)

    def test_get_search(self):
        url = reverse("book-list")
        books = (
            Book.objects.filter(id__in=[self.book1.id, self.book3.id])
            .annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg("userbookrelation__rate"),
            )
            .order_by("id")
        )
        self.client.force_login(self.user1)
        response = self.client.get(url, data={"search": "xere"})
        serializer_data = BookSerializer(books, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_delete(self):
        url = reverse("book-detail", args=(self.book1.id,))
        self.client.force_login(self.user1)
        self.book1.refresh_from_db()
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Book.objects.filter(pk=self.book1.pk).exists(), False)


class BooksRelationTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test_username_1")
        self.user1 = User.objects.create(username="test_username_2")

        self.book1 = Book.objects.create(
            name="Test book 1", price=25, author="Author 1", owner=self.user1
        )
        self.book2 = Book.objects.create(
            name="Test book 2", price=50, author="Author 2"
        )

    def test_like_and_in_bookmarks(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {
            "like": True,
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertTrue(relation.like)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {"rate": 3}

        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(relation.rate, data["rate"])

    def test_rate_wrong(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {"rate": 6}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
