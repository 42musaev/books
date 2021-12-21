from django.db.models.aggregates import Avg, Count
from django.db.models.expressions import Case, When
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializer import BookSerializer
from django.contrib.auth.models import User

from store.views import BookViewSet


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.view = BookViewSet
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")

        book1 = Book.objects.create(name="Test book1", price=25, discount=10)
        book2 = Book.objects.create(name="Test book2", price=55, discount=5)

        UserBookRelation.objects.create(
            user=user1, book=book1, like=True, rate=4.5, in_bookmarks=True
        )
        UserBookRelation.objects.create(
            user=user2, book=book1, like=True, rate=4.1, in_bookmarks=True
        )
        UserBookRelation.objects.create(user=user3, book=book1, like=True, rate=5)

        UserBookRelation.objects.create(
            user=user1, book=book2, like=True, rate=3, in_bookmarks=True
        )
        UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=2)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        queryset = self.view.queryset.filter(id__in=[book1.id, book2.id])
        data = BookSerializer(queryset, many=True).data
        excepted_data = [
            {
                "id": book1.id,
                "name": "Test book1",
                "price": "25.00",
                "discount": "10.00",
                "annotated_likes": 3,
                "rating": "4.33",
                "annotated_in_bookmarks": 2,
                "discount_price": "15.00",
            },
            {
                "id": book2.id,
                "name": "Test book2",
                "price": "55.00",
                "discount": "5.00",
                "annotated_likes": 2,
                "rating": "2.50",
                "annotated_in_bookmarks": 1,
                "discount_price": "50.00",
            },
        ]

        self.assertEqual(excepted_data, data)
