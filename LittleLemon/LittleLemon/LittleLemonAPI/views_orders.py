import json
from sqlite3 import enable_callback_tracebacks
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers_order import OrderSerializer, OrderSerializerForCreate,  OrderSerializerForDeliveryCrew, OrderSerializerReadonly, OrderSerializerForManager
from .permissions import IsUserInDeliveryCrewGroup, IsUserInManagerGroup
from .models import Order

class OrderGetPost(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        currentUser = self.request.user
        # IsMAnagerOrAdmin Returns all orders with order items by all users
        if IsUserInManagerGroup(currentUser):
            orders_items = Order.objects.all()
        # Delivery crew Returns all orders with order items assigned to the delivery crew 
        elif IsUserInDeliveryCrewGroup(currentUser):
            orders_items = Order.objects.filter(delivery_crew = currentUser)
        # Returns all orders with order items created by authenticated user
        else:
            orders_items = Order.objects.filter(user = currentUser)
            
        return orders_items
    
    def get_serializer_class(self):
        if self.request.method == "POST": 
            return OrderSerializerForCreate 
        else:
            return OrderSerializer
        
class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    
    def get_object(self):
        requestedOrder : Order = super().get_object()
        currentUser = self.request.user
        # manager or admin can get any order
        if IsUserInManagerGroup(currentUser) or currentUser.is_staff :
            return requestedOrder
        # delivery crew should see only assigned orders
        if IsUserInDeliveryCrewGroup(currentUser) and requestedOrder.delivery_crew != currentUser :
                raise PermissionDenied(detail=f"Delivery Crew [{currentUser.username}] has no permissions for requested order", code=403)
        # non-Manager and non-Admin user should see only theirs order
        if requestedOrder.user != currentUser : 
                raise PermissionDenied(detail=f"Customer [{currentUser.username}] has no permissions for requested order", code=403)
        
        return requestedOrder
        
    def get_serializer_class(self):
        user = self.request.user
        
        if IsUserInDeliveryCrewGroup(user):
            return OrderSerializerForDeliveryCrew
        if IsUserInManagerGroup(user) or user.is_staff:
            return OrderSerializerForManager
        else:
            return OrderSerializerReadonly