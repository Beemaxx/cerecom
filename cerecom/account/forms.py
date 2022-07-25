from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _




class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(label = 'Username', min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you need a valid email.'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeated Password', widget=forms.PasswordInput)
    
    class Meta:
        model = UserBase
        fields = ('user_name', 'email')
        
    
    def clean_username(self):
        
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already existed.")
        return user_name
    
    def clean_password2(self):
        
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError("Passwords do not match.")
        return clean_data['password2']
    
    def clean_email(self):
        
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email  
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user_name'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Username'})
            self.fields['email'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
            self.fields['password'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Password'})
            self.fields['password2'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Repeat Password'})
            
            
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 
               'placeholder': 'Username', 
               'id': 'login-user-name'}
    ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3',
               'placeholder': 'Password',
               'id': 'login-pwd',
               }
    ))
    
    
class UserEditForm(forms.ModelForm):
    
    email = forms.EmailField(
        label='Account Email can not be changed',
        max_length=200,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'email',
                'id': 'form-email',
                'readonly':'readonly'
            }
        )
    )
    user_name = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Username',
                'id': 'form-firstname'
            }
        )
    )
    first_name = forms.CharField(
        label='Full Name',
        min_length=4,
        max_length=50,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Firstname',
                'id': 'form-lastname'
            }
        )
    )
    
    country = CountryField(
    )
    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'user_name', 'country','about')
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user_name'].required = True
            self.fields['email'].required = True
             


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email',
            }
        )
    ) 
        
    def clean_email(self):
        
        email = self.cleaned_data['email'].lower()
        u = UserBase.object.filter(email=email)
        
        if not u:
            raise forms.ValidationError(
                'Please try the correct email.'
            )
            
        return email
    

class PwdResetConfirmForm(SetPasswordForm):
        
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3',
                'placeholder': 'Password',
                'id': 'form-new-pass1',
                }
        ))
    
    new_password2 = forms.CharField(label=_("Re-enter password"), widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3',
               'placeholder': 'Repeated Password',
               'id': 'form-new-pass2',
               }
        ))
          
    def clean_password2(self):
            
            clean_data = self.cleaned_data
            if clean_data['new_password1'] != clean_data['new_password2']:
                raise forms.ValidationError("Passwords do not match.")
            return clean_data['new_password2']