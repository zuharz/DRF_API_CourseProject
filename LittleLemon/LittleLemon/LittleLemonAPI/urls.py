from django.urls import path
from . import views, views_groups_mngr, views_cart

urlpatterns = [
    path('groups/manager/users', views_groups_mngr.ManagerGroupActionsView.as_view()),
    path('groups/manager/users/<int:pk>', views_groups_mngr.ManagerGroupActionsView.as_view()),
    path('groups/delivery-crew/users', views_groups_mngr.DeliveryGroupActionsView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views_groups_mngr.DeliveryGroupActionsView.as_view()),
    
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    
    path('cart/menu-items',views_cart.CartItemsView.as_view())
]