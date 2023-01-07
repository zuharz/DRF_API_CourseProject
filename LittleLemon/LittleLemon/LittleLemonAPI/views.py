from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .permissions import IsManagerUser, IsManagerOrAdminUser
from django.shortcuts import get_object_or_404
#
# Categories endpoints
#
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    #permissions logic
    def get_permissions(self):  
        if(self.request.method=='GET'):
            return [IsAuthenticated()]
        return [IsManagerOrAdminUser()]

class CaterogyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    permission_classes = [IsManagerOrAdminUser,]
#
# Menu-items endpoints
#
class MenuItemListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    ordering_fields = ['price',]
    
    def get_permissions(self):  
        if(self.request.method=='GET'):
            return [IsAuthenticated()]
        return [IsManagerOrAdminUser()]

class MenuItemListByCategory(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        categoryId = self.kwargs.get("pk")
        category = get_object_or_404(Category, pk=categoryId)
        queryset = MenuItem.objects.filter(category=category)
        
        return queryset
    

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer