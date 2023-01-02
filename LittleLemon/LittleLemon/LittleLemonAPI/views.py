from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .permissions import IsManagerUser, IsManagerOrAdminUser
#
# Menu-items endpoints
#
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    # ordering_fields = ['price','inventory']
    # filterset_fields = ['price','inventory']
    # search_fields=['title']
    
    #permissions logic
    def get_permissions(self):  
        if(self.request.method=='GET'):
            return [IsAuthenticated()]
        return [IsManagerOrAdminUser()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer