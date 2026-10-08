from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import obtener_estrategia


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='precio-final', url_name='precio-final')
    def precio_final(self, request, pk=None):
        producto = self.get_object()
        estrategia = obtener_estrategia(producto.category.name)
        precio_con_descuento = estrategia.calcular(float(producto.price))

        return Response({
            'producto': producto.name,
            'precio_original': producto.price,
            'precio_final': round(precio_con_descuento, 2)
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

