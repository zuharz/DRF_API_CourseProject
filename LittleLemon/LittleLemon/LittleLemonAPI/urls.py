from django.urls import path
from . import views, views_groups, views_cart, views_orders

urlpatterns = [
    path('groups/manager/users', views_groups.ManagerGroupGetPost.as_view()),
    path('groups/manager/users/<int:pk>', views_groups.ManagerGroupActionsView.as_view()),
    path('groups/delivery-crew/users', views_groups.DeliveryGroupGetPost.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views_groups.DeliveryGroupActionsView.as_view()),
    
    path('category', views.CategoriesView.as_view()),
    path('category/<int:pk>', views.CaterogyView.as_view()),
    path('menu-items', views.MenuItemListCreate.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items/category/<int:pk>', views.MenuItemListByCategory.as_view()),
    
    path('cart/menu-items',views_cart.CartGetPostDelete.as_view()),
    
    path('orders', views_orders.OrderGetPost.as_view()),
    path('orders/<int:pk>', views_orders.OrderRetrieveUpdateDestroy.as_view())
]