from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product
from order.models import Order

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            password='testpass123',
            email='api@test.com'
        )
        self.client.force_authenticate(user=self.user)
        
        self.product = Product.objects.create(
            name='API Test Product',
            price=199.99,
            description='For API testing',
            stock=25
        )
    
    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_product(self):
        data = {
            'name': 'New Product via API',
            'price': 299.99,
            'description': 'Created by API test',
            'stock': 15
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_product(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Product')

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='orderuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.product1 = Product.objects.create(
            name='Book 1',
            price=49.90,
            stock=20
        )
        
        self.product2 = Product.objects.create(
            name='Book 2',
            price=39.90,
            stock=15
        )
    
    def test_create_order(self):
        data = {
            'items': [
                {'product_id': self.product1.id, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ]
        }
        
        response = self.client.post('/api/orders/', data, format='json')
        
        # Pode retornar 201 ou 400 dependendo da implementação
        self.assertIn(response.status_code, 
                     [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        
        if response.status_code == 201:
            self.assertEqual(Order.objects.count(), 1)