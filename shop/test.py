from django.urls import reverse_lazy, reverse
from itsdangerous import json
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import Category, Product
from shop.mocks import mock_openfoodfact_success, ECOSCORE_GRADE
from unittest import mock

'''
class ShopAPITestCase(APITestCase):
    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaîne de caractères sous le même format que celui de l'api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_article_list_data(self, articles):
        return [
            {
                'id' : article.pk,
                'name' : article.name,
                'price' : article.price,
                'date_created' : self.format_datetime(article.date_created),
                'date_updated' : self.format_datetime(article.date_updated),
                'product' : self.product_id
            } for article in articles
        ]

    def get_product_detail_data(self, product):
        # Modifions les données attendues pour le détail d'un produit en ajoutant l'écoscore
        return {
            'id' : product.pk,
            'name' : product.name,
            'date_created' : self.format_datetime(product.date_created),
            'date_updated' : self.format_datetime(product.date_updated),
            'category' : product.category_id,
            'articles' : self.get_article_list_data(product.articles.filter(active=True)),
            'ecoscore' : ECOSCORE_GRADE  # la valeur de l'ecoscore provient de notre constante utilisée dans notre mock
        }

class TestCategory(ShopAPITestCase):
    # Nous stockons l'url de l'endpoint dans un attribut de classe pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')

    def test_list(self):
        # Créons deux catégories dont une seule est active
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        # On réalise l'appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)

        # On vérifie que le status code est bien 200 et que les bonnes valeurs sont bien retournées
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id' : category.pk,
                'name' : category.name,
                'date_created' : self.format_datetime(category.date_created),
                'date_updated' : self.format_datetime(category.date_updated),
            }
        ]
        self.assertEqual(response.json(), expected)

    def test_create(self):
        # Vérifions qu'aucune catégorie n'existe avant d'en créer une
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Vérifions que le status code est bien en erreur (405) et qu'on nous empêche de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        # Vérifions qu'aucune nouvelle catégorie n'a été créée malgré le status 405
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    url = reverse_lazy('product-list')

    def create_products(self):
        category = Category.objects.create(name='Fruits', active=True)
        #product = category.products.create(name='Name 1', active=True)
        product = Product.objects.create(name='Name 1', category=category, active=True)
        Product.objects.create(name='Name 2', category=category, active=False)
        return product

    def test_list(self):
        product = self.create_products()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                'id' : product.pk,
                'name' : product.name,
                'date_created' : self.format_datetime(product.date_created),
                'date_updated' : self.format_datetime(product.date_updated),
                'category' : product.category.pk
            }
        ]
        self.assertEqual(response.json(), expected)
    
    def test_detail(self):
        product = self.create_products()
        response = self.client.get(self.url + f'{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'id' : product.pk,
            'name' : product.name,
            'date_created' : self.format_datetime(product.date_created),
            'date_updated' : self.format_datetime(product.date_updated),
            'category' : product.category_id
        }
        self.assertEqual(response.json(), expected)

    def test_filter(self):
        product = self.create_products()
        response = self.client.get(self.url, {'category_id': product.category_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                'id' : product.pk,
                'name' : product.name,
                'date_created' : self.format_datetime(product.date_created),
                'date_updated' : self.format_datetime(product.date_updated),
                'category' : product.category_id
            }
        ]
        self.assertEqual(response.json(), expected)

    def test_create(self):
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouveau produit'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertFalse(Product.objects.exists())

    def test_modify(self):
        product = self.create_products()
        response = self.client.put(self.url + f'{product.pk}/', data={'name': 'Update du produit'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(Product.objects.get(id=product.pk).name, 'Update du produit')
        response = self.client.get(self.url + f'{product.pk}/', follow=True)
        not_expected = [
            {
                'id' : 'Update du produit',
                'name' : product.name,
                'date_created' : self.format_datetime(product.date_created),
                'date_updated' : self.format_datetime(product.date_updated),
                'category' : product.category_id
            }
        ]
        self.assertNotEqual(response.json(), not_expected)

    def test_delete(self):
        product = self.create_products()
        self.assertTrue(Product.objects.filter(id=product.pk).exists())
        response = self.client.delete(self.url + f'{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Product.objects.filter(id=product.pk).exists())
'''

from unittest import mock

from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product
from shop.mocks import mock_openfoodfact_success, ECOSCORE_GRADE


class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_article_list_data(self, articles):
        return [
            {
                'id': article.pk,
                'name': article.name,
                'date_created': self.format_datetime(article.date_created),
                'date_updated': self.format_datetime(article.date_updated),
                'product': article.product_id
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id,
                'ecoscore': ECOSCORE_GRADE
            } for product in products
        ]

    def get_category_list_data(self, categories):
        return [
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in categories
        ]


class TestCategory(ShopAPITestCase):

    url = reverse_lazy('category-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        for r in range(len(response.json())):
            self.assertEqual(response.json()[r], self.get_category_list_data([self.category, self.category_2]))

    def test_create(self):
        category_count = Category.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Category.objects.count(), category_count)


class TestProduct(ShopAPITestCase):

    url = reverse_lazy('product-list')

    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for r in range(len(response.json())):
            self.assertEqual(self.get_product_list_data([self.product, self.product_2]), response.json()[r])

    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        for r in range(len(response.json())):
            self.assertEqual(self.get_product_list_data([self.product]), response.json()[r])

    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()