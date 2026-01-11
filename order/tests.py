from django.test import TestCase
from django.contrib.auth.models import User
from product.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, CreateOrderItemSerializer

class OrderModelTest(TestCase):
    """Testes para os modelos Order e OrderItem"""
    
    def setUp(self):
        """Configuração comum para os testes"""
        self.user = User.objects.create_user(
            username='cliente',
            password='senha123',
            email='cliente@teste.com'
        )
        self.product = Product.objects.create(
            name='Livro de Teste',
            price=49.90,
            stock=100
        )
    
    def test_create_order(self):
        """Testa criação de um pedido"""
        order = Order.objects.create(
            user=self.user,
            total_amount=99.80,
            status='pending'
        )
        
        self.assertEqual(order.user.username, 'cliente')
        self.assertEqual(float(order.total_amount), 99.80)
        self.assertEqual(order.status, 'pending')
        self.assertIsNotNone(order.created_at)
    
    def test_create_order_item(self):
        """Testa criação de um item de pedido"""
        order = Order.objects.create(user=self.user)
        
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
        
        self.assertEqual(order_item.product.name, 'Livro de Teste')
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(float(order_item.unit_price), 49.90)
    
    def test_order_item_subtotal(self):
        """Testa o cálculo do subtotal do item"""
        order = Order.objects.create(user=self.user)
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            unit_price=30.00
        )
        
        expected_subtotal = 90.00  # 3 * 30.00
        self.assertAlmostEqual(float(order_item.subtotal), expected_subtotal, places=2)

class OrderSerializerTest(TestCase):
    """Testes para os serializers de Order"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='serializertest')
        self.product = Product.objects.create(
            name='Produto Serializer',
            price=75.50,
            stock=50
        )
        
        self.order = Order.objects.create(
            user=self.user,
            total_amount=151.00,  # 2 * 75.50
            status='processing'
        )
        
        # Adiciona um item ao pedido
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=75.50
        )
    
    def test_order_serializer(self):
        """Testa o OrderSerializer básico"""
        serializer = OrderSerializer(self.order)
        
        self.assertEqual(serializer.data['id'], self.order.id)
        self.assertEqual(serializer.data['status'], 'processing')
        self.assertAlmostEqual(float(serializer.data['total_amount']), 151.00, places=2)
        self.assertEqual(len(serializer.data['items']), 1)
    
    def test_create_order_item_serializer(self):
        """Testa o serializer para criar items"""
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
        serializer = CreateOrderItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Erros: {serializer.errors}")
        
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['product_id'], self.product.id)
        self.assertEqual(validated_data['quantity'], 3)
    
    def test_order_create_serializer_structure(self):
        """Testa a estrutura do OrderCreateSerializer"""
        # Verifica se o serializer tem o campo 'items'
        serializer = OrderCreateSerializer()
        self.assertIn('items', serializer.fields)
        
        # Testa com dados válidos
        data = {
            'items': [
                {'product_id': self.product.id, 'quantity': 2}
            ]
        }
        
        # Como não temos request context, não podemos chamar create()
        # mas podemos validar a estrutura
        serializer = OrderCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Erros: {serializer.errors}")