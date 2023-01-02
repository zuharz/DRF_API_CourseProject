from email.headerregistry import Group
from tokenize import Double
from unicodedata import decimal
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User, Group
import bleach

from .models import Category, MenuItem, Cart, Order, OrderItem

class GroupNameField(serializers.RelatedField):
    def to_representation(self, value):
        # Return the group name
        return value.name

class UserSerializer(serializers.ModelSerializer):
    groups = GroupNameField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups')

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta():
        model = MenuItem
        fields = ['id','title','price','featured', 'category', 'category_id']
        
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']

        extra_kwargs = {
                'quantity': {'min_value': 1},
                'unit_price':{'min_value': 0.1}
            }
    
    def create(self, validated_data):
        #set current logged in user 
        request = self.context['request']
        user = request.user
        validated_data['user'] = user
        #calculate
        price = self.__calculatePrice(validated_data['quantity'], validated_data['unit_price'])
        validated_data['price'] = price
        return super().create(validated_data)
    
    def __calculatePrice(self, quantity, unit_price):
        return quantity * unit_price