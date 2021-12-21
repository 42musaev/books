from django.db.models.aggregates import Avg, Count
from django.db.models.expressions import Case, When
from django.shortcuts import render
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from store.models import Book, UserBookRelation
from store.permisions import IsOwnerOrReadOnly
from store.serializer import BookSerializer, UserBookRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(ModelViewSet):
    queryset = (
        Book.objects.all()
        .annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg("userbookrelation__rate"),
        )
        .order_by("id")
    )
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["price"]
    search_fields = ["name", "author"]
    ordering_fields = ["price", "author"]
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = "book"

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(
            user_id=self.request.user.id, book_id=self.kwargs["book"]
        )
        return obj


def auth(request):
    return render(request, "oauth.html")
