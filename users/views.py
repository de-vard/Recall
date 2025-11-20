from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response

from users.models import Follow
from users.permissions import IsAuthor
from users.serializers import UserSerializer, UserSerializerRetrieve, MeSerializerRetrieve

User = get_user_model()


class UserAPIView(generics.ListAPIView):
    """Возвращает список всх пользователей """
    queryset = User.objects.all().only('public_id', 'username', 'avatar')
    serializer_class = UserSerializer


class UserAPIRetrieve(generics.RetrieveAPIView):
    """Детальная информация об чужом профиля"""
    queryset = User.objects.all().only(
        'public_id', 'username',
        'first_name', 'last_name', 'avatar',
    ).prefetch_related('authored_courses')

    serializer_class = UserSerializerRetrieve
    lookup_field = 'public_id'  # Указываем, что ищем по полю public_id


class MeAPIRetrieve(generics.RetrieveUpdateDestroyAPIView):
    """Детальная информация своего профиля"""
    queryset = User.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = MeSerializerRetrieve
    lookup_field = 'public_id'  # Указываем, что ищем по полю public_id


class FollowUserAPI(APIView):
    """Подписка на курс"""
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, public_id):
        user_to = get_object_or_404(User, public_id=public_id)
        user_from = request.user
        if user_from == user_to:
            return Response({"detail": "Нельзя подписаться на самого себя."}, status=400)
        elif Follow.objects.filter(user_from=user_from, user_to=user_to).exists():
            return Response({"detail": "Вы уже подписаны."}, status=400)
        else:
            Follow.objects.create(user_from=user_from, user_to=user_to)

        return Response({"detail": "Успешно подписано!"}, status=201)


class UnfollowUserAPI(APIView):
    """Подписка на курс"""
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, public_id):
        user_to = get_object_or_404(User, public_id=public_id)
        user_from = request.user
        follow = Follow.objects.filter(user_from=user_from, user_to=user_to).first()
        if not follow:
            return Response({"detail": "Вы не подписаны."}, status=400)

        follow.delete()
        return Response({"detail": "Успешно отписано!"}, status=200)
