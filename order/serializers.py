from rest_framework import serializers
from django.contrib.auth.models import User
from product.models import Product
from product.serializers import ProductSerializer
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 
                 'unit_price', 'subtotal']
        read_only_fields = ['unit_price']
    
    def get_subtotal(self, obj):
        return obj.subtotal

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'status_display',
                 'items', 'created_at']
        read_only_fields = ['total_amount', 'created_at']

# ADICIONE ESTAS CLASSES QUE ESTAVAM FALTANDO:
class CreateOrderItemSerializer(serializers.Serializer):
    """Serializer para criar items no pedido"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    """Serializer para criar um novo pedido"""
    items = CreateOrderItemSerializer(many=True, min_length=1)
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")
        
        # Cria o pedido
        order = Order.objects.create(
            user=request.user,
            status='pending',
            total_amount=0
        )
        
        total = 0
        items_data = validated_data['items']
        
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Produto com ID {item_data['product_id']} não encontrado"
                )
            
            # Verifica estoque
            if product.stock < item_data['quantity']:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para {product.name}"
                )
            
            # Cria o item do pedido
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.price
            )
            
            total += float(order_item.subtotal)
        
        # Atualiza total do pedido
        order.total_amount = total
        order.save()
        
        return order