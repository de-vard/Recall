from django.contrib.auth import get_user_model
from rest_framework import mixins

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend_apps.users.models import Follow
from backend_apps.users.permissions import IsAuthor
from backend_apps.users.serializers import UserSerializer, UserSerializerRetrieve, MeSerializerRetrieve

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                  GenericViewSet):
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.action == "list":
            return User.objects.all().only(
                "public_id", "username", "avatar"
            )

        # detail + follow/unfollow
        return User.objects.all().select_related().prefetch_related(
            "authored_courses"
        )

    def get_permissions(self):
        """Ограничение по методам"""
        # Словарь соответствия действий и разрешений
        permission_map = {
            'list': [IsAuthenticated],
            'retrieve': [IsAuthenticated],
            'update': [IsAuthor],  # автор ли
            'partial_update': [IsAuthor],  # автор ли
            'destroy': [IsAuthor],  # автор ли
            'metadata': [IsAuthenticated],  # метаданные
            'subscribe_unsubscribe': [IsAuthenticated],
            'like_dislike': [IsAuthenticated],
        }

        # Получаем permission_classes для текущего действия или пустой список по умолчанию
        permission_classes = permission_map.get(self.action, [])

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        # Swagger вызывает view без kwargs, для того что бы swagger не давал ошибку
        if getattr(self, "swagger_fake_view", False):
            return UserSerializer

        if self.action == "list":
            return UserSerializer
        if self.action == "retrieve":
            # если пользователь смотрит на себя → свой сериализатор
            if self.get_object() == self.request.user:
                return MeSerializerRetrieve
            return UserSerializerRetrieve

        return UserSerializerRetrieve

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, public_id=None):
        user_to = self.get_object()
        user_from = request.user

        if user_to == user_from:
            return Response({"detail": "Нельзя подписаться на самого себя."}, status=400)

        follow = Follow.objects.filter(user_from=user_from, user_to=user_to).first()

        # если нет — подписываем
        if not follow:
            Follow.objects.create(user_from=user_from, user_to=user_to)
            return Response({"detail": "Подписка оформлена!"}, status=201)

        # если есть — отписываем
        follow.delete()
        return Response({"detail": "Отписка выполнена!"}, status=200)
