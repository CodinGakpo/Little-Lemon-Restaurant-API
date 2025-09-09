from django.urls import path,include
from .views import *

urlpatterns = [
    path('menu-items/', MenuItemView.as_view({'get': 'list', 'post': 'create'}), name='menu_items'),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='menu_items_detail'),
    path('groups/manager/users/', ManagerViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='manager'),
    path('groups/delivery-crew/users/', DeliveryCrewViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='delivery_crew'),
    path('cart/menu-items/', CartViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='cart'),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='order'),
    path('orders/<int:pk>/', OrderManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'})),
    path("users/", UserCreateView.as_view(), name="user-register"),
    path("users/user/me/", CurrentUserView.as_view(), name="current-user"),
    path("token/", include("djoser.urls.authtoken")),

]
