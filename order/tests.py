from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, OrderItem
from product.models import Product, Category


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="João Silva",
            customer_email="joao@email.com"
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.customer_name, "João Silva")
        self.assertEqual(self.order.status, 'pending')


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='will', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name='Ficção')
        self.product = Product.objects.create(
            title='1984',
            author='George Orwell',
            price=35.00,
            category=self.category,
            stock=10
        )
        self.order_data = {
            'customer_name': 'Maria Santos',
            'customer_email': 'maria@email.com',
            'status': 'pending'
        }
    
    def test_create_order(self):
        url = reverse('order-list')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
    
    def test_get_orders(self):
        Order.objects.create(**self.order_data)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_order(self):
        order = Order.objects.create(**self.order_data)
        url = reverse('order-detail', kwargs={'pk': order.pk})
        updated_data = {
            'customer_name': 'Maria Silva',
            'customer_email': 'maria@email.com',
            'status': 'processing'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'processing')
    
    def test_delete_order(self):
        order = Order.objects.create(**self.order_data)
        url = reverse('order-detail', kwargs={'pk': order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)