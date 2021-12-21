from django.db.models.aggregates import Count
from django.db.models.expressions import Case, When
from rest_framework import serializers

from store.models import Book, UserBookRelation


class BookSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_in_bookmarks = serializers.IntegerField(read_only=True)
    discount_price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ("id", "name", "price", "discount", "annotated_likes", "annotated_in_bookmarks", "discount_price", "rating")


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
