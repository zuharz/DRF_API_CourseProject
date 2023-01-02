from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from rest_framework import status
import json

from .models import Cart
from .permissions import IsCustomerUser, IsManagerOrAdminUser
from .serializers import CartSerializer

class CartItemsView(APIView):
    permission_classes = (IsCustomerUser,)
    # /api/cart/menu-items -> Returns current items in the cart for the current user token
    def get(self, request: Request, format=None):
        
        queryset = Cart.objects.filter(user = request.user)
        serializer = CartSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # /api/cart/menu-items -> Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
    def post(self, request, format=None):
        try:
            serializer = CartSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(f"Can't add items to the cart due to the error {e}", status.HTTP_400_BAD_REQUEST)
    
    # /api/cart/menu-items -> Deletes all menu items created by the current user token
    def delete(self, request):
        # Retrieve the user from the request payload
        cartItems = Cart.objects.filter(user = request.user)
        
        itemsToDelete = cartItems.count()
        if(itemsToDelete == 0):
            return Response(f"Not items for {request.user.username} in the cart to delete", status.HTTP_200_OK)
        
        for cItem in cartItems:
            cItem.delete()

        jsonResponse = json.dumps(
            {
                'items_deleted': itemsToDelete,
                'user': request.user.username
            }
        )
        
        return Response(jsonResponse, status.HTTP_200_OK)