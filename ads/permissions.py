from rest_framework.permissions import BasePermission

from authentication.models import UserRoles


class AdChangePermission(BasePermission):
    message = "Changing for non Admin user not allowed"

    def has_object_permission(self, request, view, obj):

        if obj.author.role == view.request.data['author'] or obj.author.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        else:
            return False
