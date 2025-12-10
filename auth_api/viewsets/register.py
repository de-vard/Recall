from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from auth_api.serializers.register import RegisterSerializer


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
            Переопределяем create, чтобы:
            - провалидировать входные данные
            - создать пользователя через сериализатор
            - сразу сгенерировать JWT токены (refresh + access)
            - вернуть их вместе с данными пользователя
        """

        # Передаём в сериализатор входящие данные из запроса
        serializer = self.serializer_class(data=request.data)

        # Проверяем валидность данных; при ошибке выбрасывает исключение
        serializer.is_valid(raise_exception=True)

        # Создаём нового пользователя.
        # serializer.save() вызывает метод create() в сериализаторе,
        # который использует User.objects.create_user(...)
        user = serializer.save()

        # Генерируем JWT-токены для созданного пользователя:
        # - refresh (долгоживущий)
        # - access (короткоживущий)
        refresh = RefreshToken.for_user(user)

        # Формируем ответ:
        # - данные пользователя (serializer.data)
        # - refresh токен
        # - access токен (здесь назван "token")
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "token": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
