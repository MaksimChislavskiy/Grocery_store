from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Cart, Category, Product, SubCategory


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Тестовая категория', slug='test-cat'
        )
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Тестовая подкатегория',
            slug='test-subcat'
        )
        self.product = Product.objects.create(
            subcategory=self.subcategory,
            name='Тестовый продукт',
            slug='test-product',
            price=99.99
        )

    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_category_list(self):
        """Тест GET запроса списка категорий с подкатегориями"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        category_data = response.data['results'][0]
        self.assertIn('subcategories', category_data)
        self.assertEqual(category_data['name'], 'Тестовая категория')


class CartAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Категория')
        self.subcategory = SubCategory.objects.create(
            category=self.category, name='Подкатегория'
        )
        self.product = Product.objects.create(
            subcategory=self.subcategory,
            name='Продукт',
            price=50.00
        )

    def test_add_to_cart(self):
        url = reverse('cart')
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_get_cart_requires_auth(self):
        """Тест что доступ к корзине только для авторизованных"""
        self.client.logout()
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
