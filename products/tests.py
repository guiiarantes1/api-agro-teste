from django.test import TestCase
from products.models import Product
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_create_invalid_product(self):
        product = Product(name='', price=-10)
        with self.assertRaises(ValidationError):
            product.full_clean()  # Valida os campos antes de salvar
