# from rest_framework import permissions
#
#
# class UserUpdatePermission(permissions.BasePermission):
#     """
#     Permission class to check that a user can read and change its own profile
#     """
#
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_superuser or obj.pk == request.user.id
#
#
# class IsAdminOrIsOwner(permissions.BasePermission):
#     """
#     Permission class to check that a user can read and change its own profile
#     """
#
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_superuser or obj.registered_by == request.user
