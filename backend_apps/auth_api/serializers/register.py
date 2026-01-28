from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from conf import settings

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
        user = User.objects.create_user(**validated_data)

        # Генерируем токен для подтверждения почты
        token = user.generate_email_verification_token()

        request = self.context.get('request')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        full_url = request.build_absolute_uri(verify_url)
        send_mail(
            subject='Подтвердите регистрацию',
            message=f'Ссылка для активации (24 часа):\n{full_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user

    def to_representation(self, instance):
        return {"message": "Регистрация успешна. Проверьте почту для подтверждения email.", "email": instance.email, }
