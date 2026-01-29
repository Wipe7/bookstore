from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Ficção",
            description="Livros de ficção"
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Ficção")
        self.assertEqual(str(self.category), "Ficção")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Romance")
        self.product = Product.objects.create(
            title="Dom Casmurro",
            author="Machado de Assis",
            price=29.90,
            category=self.category,
            stock=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.title, "Dom Casmurro")
        self.assertEqual(self.product.price, 29.90)


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='will', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.category_data = {
            'name': 'Aventura',
            'description': 'Livros de aventura'
        }
    
    def test_create_category(self):
        url = reverse('category-list')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Aventura')
    
    def test_get_categories(self):
        Category.objects.create(**self.category_data)
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_category(self):
        category = Category.objects.create(**self.category_data)
        url = reverse('category-detail', kwargs={'pk': category.pk})
        updated_data = {'name': 'Ação', 'description': 'Livros de ação'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Ação')
    
    def test_delete_category(self):
        category = Category.objects.create(**self.category_data)
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='will', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Terror')
        self.product_data = {
            'title': 'It - A Coisa',
            'author': 'Stephen King',
            'price': 45.00,
            'category': self.category.id,
            'stock': 5
        }
    
    def test_create_product(self):
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_get_products(self):
        Product.objects.create(
            title='It',
            author='Stephen King',
            price=45.00,
            category=self.category,
            stock=5
        )
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_product(self):
        product = Product.objects.create(
            title='It',
            author='Stephen King',
            price=45.00,
            category=self.category,
            stock=5
        )
        url = reverse('product-detail', kwargs={'pk': product.pk})
        updated_data = {
            'title': 'It - A Coisa',
            'author': 'Stephen King',
            'price': 50.00,
            'category': self.category.id,
            'stock': 10
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.price, 50.00)
    
    def test_delete_product(self):
        product = Product.objects.create(
            title='It',
            author='Stephen King',
            price=45.00,
            category=self.category,
            stock=5
        )
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)