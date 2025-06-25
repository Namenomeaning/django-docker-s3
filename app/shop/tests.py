from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic products'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')
        self.assertEqual(str(self.category), 'Electronics')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            description='A great smartphone',
            price=Decimal('299.99'),
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Smartphone')
        self.assertEqual(self.product.price, Decimal('299.99'))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.available)
        self.assertEqual(str(self.product), 'Smartphone')


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            description='A great smartphone',
            price=Decimal('299.99'),
            stock=10
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(str(self.cart), f'Cart {self.cart.id}')

    def test_cart_total_price(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(self.cart.get_total_price(), Decimal('599.98'))

    def test_cart_total_items(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3
        )
        self.assertEqual(self.cart.get_total_items(), 3)


class ShopViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            description='A great smartphone',
            price=Decimal('299.99'),
            stock=10
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')

    def test_cart_detail_view(self):
        response = self.client.get(reverse('shop:cart_detail'))
        self.assertEqual(response.status_code, 200)
