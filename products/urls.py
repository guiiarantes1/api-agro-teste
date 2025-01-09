from django.urls import path
from .views import ProductListCreateView, ProductDeleteView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]
