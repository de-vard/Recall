"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers


from backend_apps.auth_api.viewsets.login import LoginViewSet
from backend_apps.auth_api.viewsets.refresh import RefreshViewSet
from backend_apps.auth_api.viewsets.register import RegisterViewSet
from backend_apps.auth_api.viewsets.social_login import SocialLoginView

from backend_apps.courses.views import CourseViewSet
from backend_apps.flashcards.views import CardViewSet, FlashViewSet
from backend_apps.folders.views import FolderViewSet
from backend_apps.media.views import ImageViewSet, SoundViewSet
from backend_apps.study.views import StudyAPIView, StudySessionHistoryAPIView, CardProgressHistoryAPIView
from backend_apps.users.views import UserViewSet
from .yasg import urlpatterns as doc_urls

from conf import settings

router = routers.DefaultRouter()

router.register(r'api/v1/courses', CourseViewSet, basename='course')
router.register(r'api/v1/folders', FolderViewSet, basename='folder')
router.register(r'api/v1/cards', CardViewSet, basename='card')
router.register(r'api/v1/flashcards', FlashViewSet, basename='flashcards')
router.register(r'api/v1/users', UserViewSet, basename='user')
router.register(r'api/v1/auth/register', RegisterViewSet, basename='auth-register')
router.register(r'api/v1/auth/login', LoginViewSet, basename='auth-login')
router.register(r'api/v1/auth/refresh', RefreshViewSet, basename='auth-refresh')
router.register(r"api/v1/images", ImageViewSet, basename="image")
router.register(r"api/v1/sounds", SoundViewSet, basename="sound")

urlpatterns = [
    path('api/v1/social/<str:provider>/', SocialLoginView.as_view(), name='social-login'),
    path('my-secret-admin-panel/', admin.site.urls),
    path("api/v1/study/<flashcard_set_id>/", StudyAPIView.as_view()),
    path("api/v1/study/<uuid:flashcard_set_id>/history/sessions/", StudySessionHistoryAPIView.as_view()),
    path("api/v1/study/history/cards/<uuid:card_id>/", CardProgressHistoryAPIView.as_view()),
    path('', include(router.urls)),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
