from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from shop.models import Article, Category, Product


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError('Category already exists')
        return value

    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
            # Levons une ValidationError si ce n'est pas le cas
            raise ValidationError('Name must be in description')
        return data

class CategoryDetailSerializer(ModelSerializer):
    # En utilisant un 'SerializerMethodField', il est nécessaire d'écrire une méthode nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']
        #fields = '__all__'

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que le produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductListSerializer(queryset, many=True)
        # La propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'ecoscore']

class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()
    class Meta:
         model = Product
         fields = ['id', 'name', 'date_created', 'date_updated', 'category', 'articles', 'ecoscore']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields= ['id', 'name', 'price', 'date_created', 'date_updated', 'product']

    def validate_price(self, value):
        if value < 1:
            raise ValidationError('Price must be greater than 1€')
        return value

    def validate_product(self, value):
        if not value.active:
            raise ValidationError('Product must be active')
        return value