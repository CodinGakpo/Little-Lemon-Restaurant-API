import datetime
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import APIView, permission_classes,action
from rest_framework.serializers import ModelSerializer
from .models import MenuItem,Cart,Order, OrderItem
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import *
from rest_framework import generics, status, viewsets
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

@permission_classes([IsAuthenticated, IsManagerOrReadOnly])
class MenuItemView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
@permission_classes([IsAuthenticated,IsManagerOrReadOnly])
class SingleMenuItemView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class ManagerViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated,IsManager]
    
    
    def list(self, request):
        manager_group = Group.objects.get(name='Manager')
        manager_users = manager_group.user_set.all()
        serializer = UserSerializer(manager_users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self, request):
        username = request.data.get('username')
        if not username:
            raise ValidationError({"username": "This field is required."})

        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)

        return Response({"message":"delete successful! "}, status=status.HTTP_204_NO_CONTENT)
        
class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    
    def list(self, request):
        delivery_crew_group = Group.objects.get(name='Delivery Crew')
        delivery_crew_users = delivery_crew_group.user_set.all()
        serializer = UserSerializer(delivery_crew_users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        delivery_crew = Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.add(user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        delivery_crew = Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.remove(user)

        return Response({"message":"delete successful! "}, status=status.HTTP_204_NO_CONTENT)

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def list(self, request):
        carts = Cart.objects.filter(user=request.user) 
        serializer = CartSerializer(carts, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def create(self, request):
        menuitem = get_object_or_404(MenuItem, id=request.data.get("menuitem_id"))
        quantity = request.data['quantity']
        unit_price = menuitem.price
        price = Decimal(quantity) *unit_price


        cart_item = Cart.objects.create(
                user=request.user,
                menuitem=menuitem,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        carts = Cart.objects.filter(user=request.user)
        if not carts.exists():
            raise PermissionDenied("Your cart is already empty.")

        carts.delete()
        return Response({"message":"Your cart has been emptied."}, status=status.HTTP_204_NO_CONTENT)
               
class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def list(self, request):

        if request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        elif request.user.groups.filter(name='Delivery Crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK) 
        
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK) 


    def create(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user, status=False, date=datetime.date.today())
        total_price = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            total_price += cart_item.price
        
        order.total = total_price
        order.save()
        cart_items.delete()
        serializer = OrderSerializer(order)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, id=pk)

        if order.user != request.user and not request.user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists():
            return Response({"message": "This order does not belong to you."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    def update(self, request):
        order_id = request.data.get("orderId")
        order = get_object_or_404(Order, id=order_id)
        
        if request.user.groups.filter(name='Manager').exists():
            if order.status == 0:
                order.status = 1
    
                delivery_crew_id = request.data.get('delivery_crew', None)
                if delivery_crew_id:
                    try:
                        delivery_crew = User.objects.get(pk=delivery_crew_id)
                        order.delivery_crew = delivery_crew
                    except User.DoesNotExist:
                        return Response({"message": "Delivery crew not found"}, status=status.HTTP_400_BAD_REQUEST)
                order.save()
                return Response({"message": "This order is on its way."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "This order is already out for delivery."}, status=status.HTTP_400_BAD_REQUEST)
            
        if request.user.groups.filter(name='Delivery Crew').exists():
            if order.delivery_crew != request.user:
                return Response({"message": "This order is not assigned to you."}, status=status.HTTP_403_FORBIDDEN)
            else:
                if order.status == 0:
                    order.status = 1
                    order.save()
                    return Response({"message": "Order delivery confirmed."}, status=status.HTTP_200_OK)
                else:
                    order.status = 0
                    order.save()
                    return Response({"message": "Order status updated to out for delivery."}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['delete'])
    def destroy(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied("You do not have permission to delete orders.")

        order = get_object_or_404(Order, id=request.data["orderId"])
        order.delete()
        return Response({"message": "Order successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
