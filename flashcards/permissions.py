from rest_framework import permissions

from courses.models import CourseStudent


class IsAuthor(permissions.BasePermission):
    """Автор """

    def has_object_permission(self, request, view, obj):
        return request.user.public_id == obj.course.author.public_id


class IsSubscribe(permissions.BasePermission):
    """Подписан ли пользователь на курс"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        course = obj.course
        return CourseStudent.objects.filter(user=user, course=course).exists()
