from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import CartView, CategoryListView, ProductListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]