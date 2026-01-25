import requests
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class Check:
    """Класс для проверок"""

    def __init__(self, provider, code):
        self.provider = provider
        self.code = code
        self.__check_provider()
        self.__check_code()

    def __check_provider(self):
        """Проверка какой используется провайдер"""
        if self.provider not in ('github', 'google'):
            raise ValidationError('Unsupported provider|Нет такого приложения, для регистрации')

    def __check_code(self):
        """Проверка передан ли код из соц. сетей"""
        if not self.code:
            raise ValidationError('Code is required| код от приложения отсутствует')

    def get_obj(self):
        """Возвращаем провайдер и код"""
        return self.provider, self.code


class GoogleAuthentication:
    """Получаем данные от гугла и возвращаем их для создания пользователя"""

    def __init__(self, code):
        self.code = code

    def __get_access_token(self):
        """Получаем токен доступа"""
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            headers={'Accept': 'application/json'},
            data={
                'client_id': settings.AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.AUTH_GOOGLE_OAUTH2_SECRET,
                'code': self.code,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            }, timeout=10, ).json()

        access_token = token_response.get('access_token')

        if not access_token:
            raise ValidationError({
                'error': 'google token error',
                'details': token_response
            })
        return access_token

    @staticmethod
    def __get_user_resp(access_token):
        """Получение данных пользователя из гугла"""
        return requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}, timeout=15
        ).json()

    def get_infor_user(self):
        """Возвращаем данные пользователя"""
        access_token = self.__get_access_token()
        user_data = self.__get_user_resp(access_token)
        return user_data


class GithubAuthentication:
    """Получаем данные от гитхаба и возвращаем их для создания пользователя"""

    def __init__(self, code):
        self.code = code

    def __get_access_token(self):
        """Получаем токен доступа"""
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            data={
                'client_id': settings.AUTH_GITHUB_KEY,
                'client_secret': settings.AUTH_GITHUB_SECRET,
                'code': self.code,
            }, timeout=15,
        ).json()

        access_token = token_response.get('access_token')

        if not access_token:
            raise ValidationError({
                'error': 'github token error',
                'details': token_response
            })

        return access_token

    @staticmethod
    def __get_user_resp(access_token):
        """Получение данных пользователя из гитхаба"""
        return requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}, timeout=15
        ).json()

    def get_infor_user(self):
        """Возвращаем данные пользователя"""
        access_token = self.__get_access_token()
        user_data = self.__get_user_resp(access_token)
        return user_data


class SocialLoginView(APIView):
    """Регистрация авторизация по социальным сетям"""

    def post(self, request, provider):
        provider, code = Check(provider, request.data.get('code')).get_obj()

        if provider == "google":
            user_data = GoogleAuthentication(code).get_infor_user()

            # Вытягиваем данные для пользователя
            username = user_data.get('email')  # в гугл нет логинов, поэтому подставил mail
            username = username[:username.index('@')]  # убираем домен из почты
            email = user_data.get('email')
            social_id = user_data.get('sub')
            avatar = user_data.get('picture')
        elif provider == "github":
            user_data = GithubAuthentication(code).get_infor_user()

            # Вытягиваем данные для пользователя
            username = user_data.get('login')
            email = user_data.get('email') if user_data.get('email') else f"{username} зарегистрирован через {provider}"
            social_id = str(user_data.get('id'))
            avatar = user_data.get('avatar_url')
        else:
            raise ValidationError("Unsupported provider|Не поддерживаемый провайдер")

        # Создаем или возвращаем пользователя
        user, is_new = User.objects.get_or_create(
            social_provider=provider,
            social_id=social_id,
        )

        # Если пользователь только созданный добавляем данные к нему если нет, то пропускаем
        if is_new:
            self.__set_user_data(user, username, avatar, email)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            }
        })

    @staticmethod
    def __save_avatar_from_url(user, url):
        """Скачиваем фото"""
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            user.avatar.save(f"{user.username}.jpg", ContentFile(response.content), save=False)


    def __set_user_data(self, user, username, avatar, email):
        """Устанавливаем данные пользователя"""

        # Обработка username
        if username:
            original_username = username
            while User.objects.filter(username=username).exists():
                suffix = get_random_string(4).lower()
                username = f"{original_username}_{suffix}"
            user.username = username

        # Обработка email
        if email:
            original_email = email
            while User.objects.filter(email=email).exists():
                suffix = get_random_string(6).lower()
                if '@' in original_email:
                    local_part, domain = original_email.split('@', 1)
                    email = f"{local_part}_{suffix}@{domain}"
                else:
                    email = f"{original_email}_{suffix}"
            user.email = email

        if avatar:
            self.__save_avatar_from_url(user, avatar)

        user.save()
