from rest_framework.serializers import ModelSerializer
from shop.models import Article, Category, Product

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']
        #fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
         model = Product
         fields = ['id', 'name', 'date_created', 'date_updated', 'category']

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields= ['id', 'name', 'price', 'date_created', 'date_updated', 'product']