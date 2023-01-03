from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .permissions import IsManagerUser, IsManagerOrAdminUser
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
    
    permission_classes = (IsManagerOrAdminUser,)
#
# Menu-items endpoints
#
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    ordering_fields = ['price',]
    
    #permissions logic
    def get_permissions(self):  
        if(self.request.method=='GET'):
            return [IsAuthenticated()]
        return [IsManagerOrAdminUser()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
