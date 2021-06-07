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

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Qu 1'})
        serializer_data = BookSerializer([self.book, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
