from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth.models import User

class IsManagerUser(BasePermission):
    def has_permission(self, request : Request, view):
        return bool(
            request.user and request.user.is_authenticated and IsUserInManagerGroup(request.user)
        )

class IsDeliveryCrewUser(BasePermission):
    def has_permission(self, request : Request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            IsUserInDeliveryCrewGroup(request.user)
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
            (IsUserInManagerGroup(request.user) or request.user.is_superuser)
        )
    
def IsUserInManagerGroup(user) -> bool:
    return bool( user.groups.filter(name='Manager').exists() )

def IsUserInDeliveryCrewGroup(user, ) -> bool:
    return bool( user.groups.filter(name='Delivery crew').exists() )