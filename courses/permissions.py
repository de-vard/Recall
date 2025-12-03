from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user.public_id
        author = obj.author.public_id
        return user == author
