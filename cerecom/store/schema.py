import graphene

from graphene_django import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name",
                  "slug",
                  "price",
                  "in_stock",
                  )
        
class Query(graphene.ObjectType):
    
    all_products = graphene.List(ProductType, product_name=graphene.String())
    
    def resolve_all_products(root, info, product_name):
        if product_name:
            print(Product.objects.filter(name = product_name))
            return Product.objects.filter(name = product_name)
        else:
            return Product.objects.all()

schema = graphene.Schema(query=Query)