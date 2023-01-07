from django.conf import settings
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics
from abc import ABC, abstractmethod

from .permissions import IsManagerOrAdminUser
from .serializers import UserWithGroupSerializer, UserAddToGroupSerializer

class UserInGroupGetPost(generics.ListCreateAPIView, ABC):
    permission_classes = (IsManagerOrAdminUser,)
    
    def get_queryset(self):
        groupName = self._getTargetGroupNameBasedOnPath()
        group = Group.objects.get(name=groupName)
        usersInGroup = User.objects.filter(groups=group)
        
        return usersInGroup
    
    def get_serializer_class(self,  *args, **kwargs):
        if self.request.method == "POST": 
            return UserAddToGroupSerializer
        else:
            return UserWithGroupSerializer
        
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = { "groupName" : self._getTargetGroupNameBasedOnPath() }
        return serializer_class(*args, **kwargs)   
    
    @abstractmethod
    def _getTargetGroupNameBasedOnPath(self):
        pass

class ManagerGroupGetPost(UserInGroupGetPost):
    def _getTargetGroupNameBasedOnPath(self):
        return getattr(settings, "LEMON_GROUP_MANAGER", None)
    
class DeliveryGroupGetPost(UserInGroupGetPost):
    
    def _getTargetGroupNameBasedOnPath(self):
        return getattr(settings, "LEMON_GROUP_DELIVERY", None)


class UserGroupActionsView(APIView):
    # /api/groups/{group-name}/users/{userID} -> Removes this particular user from the {group-name} group and returns 200-OK
    def delete(self, request, pk):
        # Retrieve the user from the request payload
        user = User.objects.filter(pk=pk).first()
        if(user is None):
            return Response(f"User with id {pk} can't be found", status=status.HTTP_404_NOT_FOUND)
        # Remove user from the target group
        groupName = self._getTargetGroupNameBasedOnPath()
        group = Group.objects.get(name=groupName)
        user.groups.remove(group)
        user.save()
        
        return Response(f"User with id {pk} has been removed from the {groupName} group", status=status.HTTP_200_OK)
    
    #overload this method in the child class to return target group name
    def _getTargetGroupNameBasedOnPath(self):
        return str()
      
class ManagerGroupActionsView(UserGroupActionsView):
    permission_classes = (IsManagerOrAdminUser,)
    
    def _getTargetGroupNameBasedOnPath(self):
        return getattr(settings, "LEMON_GROUP_MANAGER", None)
    
class DeliveryGroupActionsView(UserGroupActionsView):
    permission_classes = (IsManagerOrAdminUser,)
    
    def _getTargetGroupNameBasedOnPath(self):
        return getattr(settings, "LEMON_GROUP_DELIVERY", None)