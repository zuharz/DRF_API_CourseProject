from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.request import Request
from django.conf import settings

class IsManagerUser(BasePermission):
    def has_permission(self, request : Request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        )

class IsDeliveryCrewUser(BasePermission):
    def has_permission(self, request : Request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.groups.filter(name='Delivery crew').exists()
        )

class IsCustomerUser(BasePermission):
    def has_permission(self, request : Request, view):
        # Allow only authenticated users
        return bool(request.user and request.user.is_authenticated) 

class IsManagerOrAdminUser(BasePermission):
    def has_permission(self, request : Request, view):
        return bool( 
            request.user and 
            request.user.is_authenticated and 
            (request.user.groups.filter(name='Manager').exists() or request.user.is_staff)
        )