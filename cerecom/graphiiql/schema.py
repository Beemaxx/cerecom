from unicodedata import name
import graphene

from graphene_django import DjangoObjectType
from store.models import Product, Product_Category

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name",
                  "slug",
                  "price",
                  "in_stock",
                  'category_id',
                  )
        

class CategoryType(DjangoObjectType):
    class Meta:
        model = Product_Category
        fields = (
            "id",
            "name",
            "slug",
        ) 
        
class Query(graphene.ObjectType):
    
    all_products = graphene.List(ProductType, 
                                 product_name=graphene.String(),
                                 )
    
    all_category = graphene.List(CategoryType,categoryname = graphene.String())
    
    product_in_category = graphene.List(ProductType,categoryname = graphene.String())
    
    def resolve_all_products(root, info, product_name):
        if product_name:
            print(Product.objects.filter(name = product_name))
            return Product.objects.filter(name = product_name)
        else:
            return Product.objects.select_related('category_id').all()
        
        
    def resolve_all_category(root, info, categoryname):
        print(categoryname)

        if categoryname:
            category = Product_Category.objects.filter(name = categoryname)
            return category
        else:
            None

    def resolve_product_in_category(root, info, categoryname):
            print(categoryname)
            if categoryname:
                category = Product_Category.objects.get(name = categoryname)
                print(category)            
                product_in_category = Product.objects.filter(category_id=category.id).all()
                print(product_in_category)
                return product_in_category
            else:
                return None


schema = graphene.Schema(query=Query)