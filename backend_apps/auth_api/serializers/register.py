from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации, обработки запросов и создания пользователя
    """
    # Убедимся, что пароль состоит минимум из 8 символов,
    # максимум из 128, и его нельзя прочитать пользователю
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        # Список всех полей, которые могут быть включены в запрос или ответ
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Используем метод `create_user`, который мы ранее написали
        # для UserManager, чтобы создать нового пользователя.
        return User.objects.create_user(**validated_data)
