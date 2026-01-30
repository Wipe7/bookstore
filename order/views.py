from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Pedidos
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Adicionar item ao pedido"""
        order = self.get_object()
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            order.calculate_total()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Atualizar status do pedido"""
        order = self.get_object()
        status = request.data.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            return Response({'status': 'Status atualizado'})
        return Response({'error': 'Status inválido'}, status=400)