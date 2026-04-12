from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Category, Product, Cart, CartItem
from .serializers import (
    CategoryWithSubcategoriesSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemCreateUpdateSerializer
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategoryWithSubcategoriesSerializer
    pagination_class = PageNumberPagination


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('subcategory__category').all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """Добавление товара в корзину"""
        cart = self.get_cart(request.user)
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Изменение количества товара в корзине"""
        cart = self.get_cart(request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        if not product_id or quantity is None:
            return Response({'error': 'Укажите product и quantity'},
                            status=status.HTTP_400_BAD_REQUEST)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        """Удаление товара из корзины или очистка всей корзины"""
        cart = self.get_cart(request.user)
        product_id = request.data.get('product')
        if product_id:
            # Удалить конкретный товар
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.delete()
        else:
            # Очистить корзину
            cart.items.all().delete()
        return Response(CartSerializer(cart).data)
