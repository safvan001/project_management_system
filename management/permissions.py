from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == 'admin'

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method in ['POST', 'DELETE']:
            return request.user.role == 'admin'
        return request.user.role in ['admin', 'manager']

class IsAdminOrManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == 'POST':
            return request.user.role == 'admin'
        if request.method in ['PUT', 'PATCH']:
            return request.user.role in ['admin', 'manager']
        if request.method == 'DELETE':
            return request.user.role == 'admin'
        return False
