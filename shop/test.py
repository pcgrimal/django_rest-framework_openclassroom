from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaîne de caractères sous le même format que celui de l'api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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
