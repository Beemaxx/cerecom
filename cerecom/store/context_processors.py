from .models import Product_Category

def all_categories(request):
    
    return {
         'product_categories' : Product_Category.objects.all() 
    }
