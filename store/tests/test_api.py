import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializer import BookSerializer


class BookApiTest(APITestCase):

    def setUp(self) -> None:
        self.book = Book.objects.create(name='Test book 1 Qu 1', price=25, author='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55, author='Author 1')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55, author='Qu 1')
        self.user = User.objects.create(
            username='test_username'
        )

    def test_get(self):
        url = reverse('book-list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = reverse('book-list')
        data = {
            'name': 'Programming in Python 3',
            'price': 150,
            'author_name': 'Mark Summerfield'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_put(self):
        url = reverse('book-detail', args=(self.book.id,))
        data = {
            'name': self.book.name,
            'price': 75,
            'author_name': self.book.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book.refresh_from_db()
        self.assertEqual(75, self.book.price)

    def test_get_search(self):
        url = reverse('book-list')
        self.client.force_login(self.user)
        response = self.client.get(url, data={'search': 'Qu 1'})
        serializer_data = BookSerializer([self.book, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_delete(self):
        url = reverse('book-detail', args=(self.book.id,))
        self.client.force_login(self.user)
        self.book.refresh_from_db()
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Book.objects.filter(pk=self.book.pk).exists(), False)
