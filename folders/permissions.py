from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user.public_id
        owner = obj.owner.public_id
        return user == owner
