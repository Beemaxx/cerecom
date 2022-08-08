from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, request
from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .models import UserBase
from order.views import user_orders


# Create your views here.

from .forms import RegistrationForm

def account_registration(request):
    
    if request.user.is_authenticated: 
        return redirect('account:dashboard')
    
    if request.method == "POST" : 
  

        registerForm = RegistrationForm(request.POST)
        print(registerForm['user_name'])
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.username = registerForm['user_name']
            user.save()

            #Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('store/account/registration/account_activation_email.html', { 
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
        
            })
            
            user.email_user(subject = subject, message = message)
            message = 'Registration was successful and an activation email was sent.'
            context = { 'message' : message }
            return render(request, 'store/account/registration/notification_sent.html', context)
            
    else:
        registerForm = RegistrationForm()
        
    return render(request, 'store/account/registration/register.html', {'form':registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request,'store/account/registration/activation_invalid.html' )

@login_required
def dashboard(request):
    
    user_order = user_orders(request)
    auth_user = get_object_or_404(UserBase, pk=request.session['_auth_user_id'])
    
    context = { 'user_orders' : user_order,
                'name' : auth_user,
        
    }
    print(auth_user.user_name)
    print(user_order)

    # orders = users_orders(request)
    
    return render(request, 'store/account/user/dashboard.html', context
                #   { 'section':'profile', 'orders':orders}
                  )
    
    
@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data = request.POST)
        
        if user_form.is_valid():
            user_form.save()
            
    else: 
        user_form = UserEditForm(instance=request.user)
        
    return render(request, 'store/account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_users(request):
    if request.method == "POST":
    
        user = UserBase.objects.get(user_name = request.user) #get user from database
        user.is_active = False
        user.save()
        logout(request)
        
        return redirect('account:delete_confirm')
