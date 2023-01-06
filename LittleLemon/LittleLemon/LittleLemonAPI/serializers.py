from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.conf import settings

from .models import Category, MenuItem, Cart

class GroupNameField(serializers.RelatedField):
    def to_representation(self, value):
        # Return the group name
        return value.name

class UserWithGroupSerializer(serializers.ModelSerializer):
    groups = GroupNameField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups')
        
class UserAddToGroupSerializer(serializers.ModelSerializer):
    groups = GroupNameField(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = User
        fields = ('user_id', 'id', 'username', 'email', 'groups')
        read_only_fields = ('username','email', 'groups')
        
    def create(self, validated_data):
        # Retrieve the user from the request payload        
        userId = validated_data['user_id']
        user = User.objects.filter(pk=userId).first()
        if(user is None):
            raise serializers.ValidationError(f"User with id {userId} can't be found")
        
        groupName = self.context['groupName']
        # Assign user to the target group
        group = Group.objects.get(name=groupName)
        user.groups.add(group)
        user.save()
        
        return user

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())#CategorySerializer(read_only=True)
    
    class Meta():
        model = MenuItem
        fields = ['id','title','price','featured', 'category']
        
class CartSerializer(serializers.ModelSerializer):
    user = UserWithGroupSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']

        extra_kwargs = {
                'quantity': {'min_value': 1},
                'unit_price':{'min_value': 0.1}
            }
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        #calculate
        price = self.__calculatePrice(validated_data['quantity'], validated_data['unit_price'])
        validated_data['price'] = price
        return super().create(validated_data)
    
    def __calculatePrice(self, quantity, unit_price):
        return quantity * unit_price




        

