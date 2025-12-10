from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from flashcards.models import FlashCardSet, Card
from flashcards.permissions import FlashIsAuthor, FlashIsSubscribe, CardIsAuthor, CardIsSubscribe
from flashcards.serializers import FlashCardDetailSerializer, FlashCardCreateSerializer, CardDetailSerializer


class FlashViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, GenericViewSet):
    lookup_field = "public_id"

    def get_serializer_class(self):
        if self.action == "create":
            return FlashCardCreateSerializer
        return FlashCardDetailSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return (
                FlashCardSet.objects
                .only("title", "course__title", "course__public_id")
                .select_related("course")
                .prefetch_related("cards__image", "cards__sound")
            )
        if self.action in ["update", "destroy"]:
            return (
                FlashCardSet.objects.all()
                .select_related("course")
            )
        return FlashCardSet.objects.all()

    def get_permissions(self):
        """Ограничение по методам"""
        # Словарь соответствия действий и разрешений
        permission_map = {
            'list': [IsAuthenticated],
            'create': [IsAuthenticated],
            'retrieve': [FlashIsSubscribe],  # автор ли или подписан он на курс
            'update': [FlashIsAuthor],  # автор ли
            'partial_update': [FlashIsAuthor],  # автор ли
            'destroy': [FlashIsAuthor],  # автор ли
            'metadata': [IsAuthenticated],  # метаданные
            'subscribe_unsubscribe': [IsAuthenticated],
            'like_dislike': [IsAuthenticated],
        }

        # Получаем permission_classes для текущего действия или пустой список по умолчанию
        permission_classes = permission_map.get(self.action, [])

        return [permission() for permission in permission_classes]


class CardViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardDetailSerializer
    lookup_field = "public_id"

    def get_permissions(self):
        """Ограничение по методам"""
        # Словарь соответствия действий и разрешений
        permission_map = {
            'list': [IsAuthenticated],
            'create': [IsAuthenticated],
            'retrieve': [CardIsSubscribe],  # автор ли или подписан он на курс
            'update': [CardIsAuthor],  # автор ли
            'partial_update': [CardIsAuthor],  # автор ли
            'destroy': [CardIsAuthor],  # автор ли
            'metadata': [IsAuthenticated],  # метаданные
            'subscribe_unsubscribe': [IsAuthenticated],
            'like_dislike': [IsAuthenticated],
        }

        # Получаем permission_classes для текущего действия или пустой список по умолчанию
        permission_classes = permission_map.get(self.action, [])

        return [permission() for permission in permission_classes]
