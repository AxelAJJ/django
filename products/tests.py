from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Category, Product
from .services import obtener_estrategia

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        """Prueba que se pueda crear una categoría."""
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        """Prueba que se puedan listar las categorías."""
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        """Prueba que se pueda crear un producto."""
        response = self.client.post('/api/v1/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00
        })
        self.assertEqual(response.status_code, 201)

    def test_list_products(self):
        """Prueba que se puedan listar los productos."""
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        """Prueba que se pueda actualizar un producto."""
        response = self.client.put(f'/api/v1/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        """Prueba que se pueda eliminar un producto."""
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_descuento_se_aplica_con_diferentes_variantes_de_categoria(self):
        self.assertEqual(obtener_estrategia('ELECTRONICA').calcular(100), 90)
        self.assertEqual(obtener_estrategia(' ropa ').calcular(100), 80)

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)     
