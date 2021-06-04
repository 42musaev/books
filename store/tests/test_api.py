from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializer import BookSerializer


class BookApiTest(APITestCase):
    def test_get(self):
        book = Book.objects.create(name='Test book1', price=25)
        book_2 = Book.objects.create(name='Test book2', price=55)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([book, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
