from rest_framework import permissions

from backend_apps.courses.models import CourseStudent, Course


class FlashIsAuthor(permissions.BasePermission):
    """Автор """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        course_public_id = request.data.get("course")
        if not course_public_id:
            return False
        try:
            course = Course.objects.only("author_id").get(public_id=course_public_id)
        except Course.DoesNotExist:
            return False
        return course.author == request.user

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
