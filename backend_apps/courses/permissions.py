from rest_framework import permissions

from backend_apps.courses.models import CourseStudent


class IsAuthor(permissions.BasePermission):
    """Автор курса"""

    def has_object_permission(self, request, view, obj):
        user = request.user.public_id
        author = obj.author.public_id
        return user == author


class IsSubscribe(permissions.BasePermission):
    """Подписан на курс ? """

    def has_object_permission(self, request, view, obj):
        user = request.user
        author = obj.author
        return CourseStudent.objects.filter(course=obj, user=user).exists() or user == author
