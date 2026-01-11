from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # Campo calculado - CERTIFIQUE-SE QUE ESTÁ DEFINIDO
    in_stock = serializers.SerializerMethodField()
    price_with_tax = serializers.SerializerMethodField()  # ESTE CAMPO AQUI!
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'price_with_tax',  # INCLUIR AQUI TAMBÉM
                 'description', 'stock', 'in_stock', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'price': {'min_value': 0},
            'stock': {'min_value': 0}
        }
    
    def get_in_stock(self, obj):
        """Verifica se há estoque"""
        return obj.stock > 0
    
    def get_price_with_tax(self, obj):
        """Adiciona 10% de imposto"""
        if obj.price:  # Verifica se price existe
            return float(obj.price) * 1.10
        return 0
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero")
        return value
    
    def validate(self, data):
        """Validação entre campos"""
        if 'price' in data and 'stock' in data:
            if data['price'] < 10 and data['stock'] > 100:
                raise serializers.ValidationError(
                    "Produtos com grande estoque devem ter preço mínimo de R$ 10,00"
                )
        return data