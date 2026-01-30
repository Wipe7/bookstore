from rest_framework import viewsets
from bookstore.pagination import StandardResultsSetPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Categorias
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination 


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Produtos
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset