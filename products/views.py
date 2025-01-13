from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 10))  # usando decorator para salvar a request no cache por 10 minutos
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # limpa o cache do endpoint após criar um novo produto pro cache ser invalidado
            cache.clear()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            # limpa o cache do endpoint após criar um novo produto pro cache ser invalidado
            cache.clear()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
