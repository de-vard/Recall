from rest_framework import permissions

from backend_apps.courses.models import CourseStudent


class FlashIsAuthor(permissions.BasePermission):
    """Автор """

    def has_object_permission(self, request, view, obj):
        return request.user.public_id == obj.course.author.public_id


class FlashIsSubscribe(permissions.BasePermission):
    """Подписан ли пользователь на курс"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        course = obj.course
        return CourseStudent.objects.filter(user=user, course=course).exists()


class CardIsAuthor(permissions.BasePermission):
    """Автор """

    def has_object_permission(self, request, view, obj):
        return request.user.public_id == obj.flashcard.course.author.public_id


class CardIsSubscribe(permissions.BasePermission):
    """Подписан ли пользователь на курс"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        course = obj.flashcard.course
        return CourseStudent.objects.filter(user=user, course=course).exists()
