from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .forms import RegistrationForm
from .token import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .models import UserBase


# Create your views here.

from .forms import RegistrationForm

def account_registration(request):
    
    if request.user.is_authenticated: 
        return redirect('account:dashboard')
    
    if request.method == "POST" : 
        print(request.POST['user_name'])
        print(request.POST['email'])
        print(request.POST['password'])

        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
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
            return HttpResponse('Registration was successful and an activation email was sent.')
            
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
    
    # orders = users_orders(request)
    
    return render(request, 'store/account/registration/dashboard.html', 
                #   { 'section':'profile', 'orders':orders}
                  )