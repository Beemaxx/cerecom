from django.shortcuts import render

# Create your views here.


  
def basket_summary(request):
    
    template_name = "store/cart/summary.html"
        
    return render(request, template_name)