from django.test import TestCase

from store.models import Book
from store.serializer import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book = Book.objects.create(name='Test book1', price=25)
        book_2 = Book.objects.create(name='Test book2', price=55)
        data = BookSerializer([book, book_2], many=True).data
        excepted_data = [
            {
                'id': book.id,
                'name': 'Test book1',
                'price': '25.00'
            },
            {
                'id': book_2.id,
                'name': 'Test book2',
                'price': '55.00'
            },

        ]
        self.assertEqual(excepted_data, data)
