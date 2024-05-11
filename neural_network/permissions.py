from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request


class AuthorOrIsAuthenticated(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj):
        return obj.author == request.user


class AuthorOrNotHidden(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        return obj.author == request.user or obj.is_hidden == False
