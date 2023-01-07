from tokenize import Double
from rest_framework import serializers

from django.utils import timezone

from .models import Order, OrderItem, Cart

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'menuitem', 'quantity', 'unit_price', 'price')
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')

    # this method gets called for each odject in the serialized queryset
    def get_order_items(self, obj):
        order_items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data

class OrderSerializerForCreate(OrderSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')
        # allow only STATUS field to be updated
        read_only_fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')
    
    def create(self, validated_data):
        currentUser = self.context['request'].user
        # ensure there are menu items in teh cart for the authenticated user
        cartItems = Cart.objects.filter(user = currentUser)
        if(len(cartItems) == 0):
            raise serializers.ValidationError(f"User {currentUser} has no menu-items in cart. Can't create order. Please, add menu items to the cart for this user.")
        
        totalPrice = sum(cart.price for cart in cartItems)
        # create order with total as sum of all the cart items 
        newOrder = Order.objects.create(user = currentUser,
                                        status = False, # undelivered
                                        total = totalPrice,
                                        date = timezone.now().date())
        # create order items 
        for cart in cartItems:
            OrderItem.objects.create(
                order = newOrder,
                menuitem = cart.menuitem,
                quantity = cart.quantity,
                unit_price = cart.unit_price,
                price = cart.price,
            )
        #delete items from the cart
        #TODO: remove items from the cart for request.user
        
        return newOrder

class OrderSerializerForManager(OrderSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')
        # allow only STATUS and Delivery crew fields to be updated
        read_only_fields = ('id', 'user', 'total', 'date', 'order_items')

class OrderSerializerForDeliveryCrew(OrderSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')
        # allow only STATUS field to be updated
        read_only_fields = ('id', 'user', 'delivery_crew', 'total', 'date', 'order_items')

class OrderSerializerReadonly(OrderSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')
        read_only_fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')