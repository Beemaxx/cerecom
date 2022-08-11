from unicodedata import category, name
import graphene

from graphene_django import DjangoObjectType
from pkg_resources import require
from store.models import Product, Product_Category

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name",
                  "slug",
                  "price",
                  "in_stock",
                  'category_id',
                  "id",
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

#Create a new Category using Mutation

class CategoryMutation(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
        # price = graphene.Decimal(required=True)
        
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, name):
        category = Product_Category(name=name)
        category.save()
        
        return CategoryMutation(category = category )
    


#Update Product Name using mutation
class ProductMutation(graphene.Mutation):
    
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required = True)
        
    product = graphene.Field(ProductType)
    
    @classmethod
    def mutate(cls, root, info, name, id):
        product = Product.objects.get(id = id)
        product.name = name 
        product.save()
        
        return ProductMutation(product = product)


#delete Product using mutation
class ProductDelete(graphene.Mutation):
    
    class Arguments:
        id = graphene.ID()
        
    product = graphene.Field(ProductType)
    
    @classmethod
    def mutate(cls, root, info, id):
        product = Product.objects.get(id = id)
        product.delete()
        
        return


class Mutation(graphene.ObjectType):
    
    update_category = CategoryMutation.Field()
    update_product = ProductMutation.Field()
    delete_product = ProductDelete.Field()

   








schema = graphene.Schema(query=Query, mutation = Mutation)