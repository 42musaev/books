from django.db.models.aggregates import Avg, Count
from django.db.models.expressions import Case, When
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializer import BookSerializer
from django.contrib.auth.models import User


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")

        book1 = Book.objects.create(name="Test book1", price=25)
        book2 = Book.objects.create(name="Test book2", price=55)

        UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=4.5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=4.1)
        UserBookRelation.objects.create(user=user3, book=book1, like=True, rate=5)

        UserBookRelation.objects.create(user=user1, book=book2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=2)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        books = (
            Book.objects.all()
            .annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
            )
            .order_by("id")
        )
        data = BookSerializer(books, many=True).data
        excepted_data = [
            {
                "id": book1.id,
                "name": "Test book1",
                "price": "25.00",
                "annotated_likes": 3,
                'rating': '4.33'
            },
            {
                "id": book2.id,
                "name": "Test book2",
                "price": "55.00",
                "annotated_likes": 2,
                'rating': '2.50'

            },
        ]
        self.assertEqual(excepted_data, data)
