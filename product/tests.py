from django.test import TestCase
from .models import Product
from .serializers import ProductSerializer

class ProductModelTest(TestCase):
    """Testes para o modelo Product"""
    
    def test_create_product(self):
        """Testa a criação básica de um produto"""
        product = Product.objects.create(
            name="Livro de Django",
            price=89.90,
            description="Um livro sobre Django",
            stock=50
        )
        self.assertEqual(product.name, "Livro de Django")
        self.assertEqual(float(product.price), 89.90)
        self.assertEqual(product.stock, 50)
        self.assertIsNotNone(product.created_at)
    
    def test_product_string_representation(self):
        """Testa a representação em string do produto"""
        product = Product.objects.create(name="Produto Teste", price=10.00)
        self.assertEqual(str(product), "Produto Teste")

class ProductSerializerTest(TestCase):
    """Testes para o serializer de Product"""
    
    def test_serializer_with_valid_data(self):
        """Testa serializer com dados válidos"""
        data = {
            'name': 'Novo Produto',
            'price': 99.99,
            'description': 'Descrição do produto',
            'stock': 25
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Erros: {serializer.errors}")
        
        # Salva o produto
        product = serializer.save()
        self.assertEqual(product.name, 'Novo Produto')
        self.assertEqual(product.stock, 25)
    
    def test_serializer_invalid_price(self):
        """Testa preço negativo no serializer"""
        data = {
            'name': 'Produto Inválido',
            'price': -5.00,
            'stock': 10
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
    
    def test_serializer_in_stock_field(self):
        """Testa o campo calculado in_stock"""
        product = Product.objects.create(name="Teste", price=10.00, stock=5)
        serializer = ProductSerializer(product)
        
        # Verifica se o campo 'in_stock' existe
        self.assertIn('in_stock', serializer.data)
        self.assertTrue(serializer.data['in_stock'])
        
        # Testa sem estoque
        product.stock = 0
        product.save()
        serializer = ProductSerializer(product)
        self.assertFalse(serializer.data['in_stock'])
    
    def test_serializer_price_with_tax_field(self):
        """Testa se o campo price_with_tax existe e calcula corretamente"""
        product = Product.objects.create(name="Teste", price=100.00, stock=10)
        serializer = ProductSerializer(product)
        
        # Primeiro verifica se o campo existe
        self.assertIn('price_with_tax', serializer.data)
        
        # Preço com 10% de imposto
        expected_price = 110.00
        self.assertAlmostEqual(serializer.data['price_with_tax'], expected_price, places=2)
    
    def test_serializer_missing_required_field(self):
        """Testa serializer sem campo obrigatório"""
        data = {
            'price': 50.00,
            'stock': 10
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)