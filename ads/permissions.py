from rest_framework.permissions import BasePermission

from authentication.models import UserRoles


class AdChangePermission(BasePermission):
    message = "Adding for non Admin user not allowed"

    def has_permission(self, request, view):
        if request.user.id == view.request.data['author']:
            return True
        elif request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        else:
            return False
