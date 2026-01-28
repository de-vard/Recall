from datetime import timedelta

from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

User = get_user_model()


class VerifyEmailView(APIView):
    """Подтверждение, что почта актуальная"""
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Функция для декодирования Base64, безопасного для URL
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Неверная ссылка"}, status=400)

        # Проверяем токен и срок действия (24 часа)
        if user.email_verification_token != token:
            return Response({"error": "Токен неверный"}, status=400)

        if user.email_verification_sent_at is None:
            return Response({"error": "Токен устарел"}, status=400)

        if timezone.now() > user.email_verification_sent_at + timedelta(hours=24):
            return Response({"error": "Ссылка истекла. Запросите повторную отправку."}, status=400)

        user.is_active = True
        user.is_email_verified = True
        user.email_verification_token = None
        user.email_verification_sent_at = None
        user.save()

        return Response({
            "message": "Email успешно подтверждён! Теперь вы можете войти в аккаунт."
        }, status=200)


class ResendVerificationEmailAPIView(APIView):
    """Повторный запрос на подтверждение почты"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Поле email обязательно"}, status=400)

        try:
            user = User.objects.get(email=email, is_email_verified=False)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден или email уже подтверждён"}, status=400)

        token = user.generate_email_verification_token()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        full_url = request.build_absolute_uri(verify_url)

        send_mail(
            subject='Повторная отправка: подтвердите регистрацию',
            message=f'Ссылка для активации (действует 24 часа):\n{full_url}',
            from_email='no-reply@yoursite.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"message": "Письмо с подтверждением отправлено повторно"})
