from rest_framework import serializers

from store.models import Book, UserBookRelation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'price',
        )


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = (
            'book',
            'like',
            'in_bookmarks',
            'rate'
        )
