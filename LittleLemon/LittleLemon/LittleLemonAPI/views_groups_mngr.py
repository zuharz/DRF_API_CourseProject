from django.conf import settings
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsManagerOrAdminUser
from .serializers import UserSerializer

class UserGroupActionsView(APIView):
    # /api/groups/{group-name}/users -> Returns all users from the {group-name}
    def get(self, request, format=None):
        groupName = self._getTargetGroupNameBasedOnPath()
        group = Group.objects.get(name=groupName)
        users = User.objects.filter(groups=group)
        
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # /api/groups/{group-name}/users -> Assigns the user in the payload to the {group-name} group and returns 201-Created
    def post(self, request, format=None):
        # Retrieve the user from the request payload
        userId = request.data.get('user_id')
        user = User.objects.filter(pk=userId).first()
        if(user is None):
            return Response(f"User with id {userId} can't be found", status=status.HTTP_404_NOT_FOUND)
        # Determine group from the request path
        groupName = self._getTargetGroupNameBasedOnPath()
        # Assign user to the target group
        group = Group.objects.get(name=groupName)
        user.groups.add(group)
        user.save()

        return Response(f"User with id {userId} was added to the {groupName} group", status=status.HTTP_201_CREATED)
    
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