from rest_framework import generics

from flashcards.models import FlashCardSet, Card
from flashcards.permissions import IsAuthor, IsSubscribe
from flashcards.serializers import FlashCardDetailSerializer, FlashCardCreateSerializer, CardDetailSerializer


class FlashCardDetailAPIView(generics.RetrieveAPIView):
    """Просмотр содержимого урока/модуля"""
    permission_classes = [IsSubscribe]
    queryset = FlashCardSet.objects.only("title", "course__title", "course__public_id") \
        .select_related("course").prefetch_related(
        "cards__image",
        "cards__sound"
    )
    serializer_class = FlashCardDetailSerializer
    lookup_field = "public_id"


class FlashCardUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Редактирование или удаление модуля"""
    permission_classes = [IsAuthor]
    queryset = FlashCardSet.objects.all().select_related("course").prefetch_related(
        "cards__image",
        "cards__sound"
    )
    serializer_class = FlashCardDetailSerializer
    lookup_field = "public_id"


class FlashCardCreateAPIView(generics.CreateAPIView):
    """Создание курса"""
    queryset = FlashCardSet.objects.all()
    serializer_class = FlashCardCreateSerializer


class CardUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Редактирование или удаление карточки"""
    queryset = Card.objects.all()
    serializer_class = CardDetailSerializer
    lookup_field = "public_id"


class CardCreateAPIView(generics.CreateAPIView):
    """Создание карта"""
    queryset = FlashCardSet.objects.all()
    serializer_class = CardDetailSerializer
