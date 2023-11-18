from django import forms
from .models import Company
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth


User = get_user_model()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length = 20,

    )
    last_name = forms.CharField(
        max_length=20,
    )
    email = forms.EmailField(
        max_length = 30,

    )
    choices = tuple(list((company.name,company.name) for company in Company.objects.all()))
    company = forms.ChoiceField(
        choices = choices,
    )

    password = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'password',
                
                'placeholder' : 10*'x' ,

            }
        )
    )
    """re_enter_password = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'type':'password',
                'id' : 're_enter_password',
                'placeholder' : 10*'x',

            }
        )
    )


"""
    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email = email)
        if users:
            raise forms.ValidationError('Email already in use')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
#        password_again = self.cleaned_data.get('re_enter_password')
        if len(password) >= 8 :
            if password.isalnum() :
                return password
            raise forms.ValidationError('Password should be a combination of letters and numbers')
        raise forms.ValidationError('password must be at least 8 characters')
    

    class LoginForm(forms.Form):
        username = forms.CharField(
        widget= forms.TextInput(
                attrs={
                    'id': 'username',
                    'placeholder' : 'username or email' ,
                    
                }
            )
        )

        password = forms.CharField(
            widget = forms.TextInput(
                attrs={
                    'type':'password',
                    'id': 'password',
                    'placeholder' : 10*'x' ,

                }
            )
        )

        def clean_username(self):
            username = self.cleaned_data.get('username')
            obj_username = User.objects.filter(username = username )
            if obj_username:
                return username
            raise forms.ValidationError("username does'nt exist")
        
        def clean_password(self):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            obj = User.objects.filter(username = username)
            if obj:
                user = auth.authenticate(username = username,password = password )
                if user!=None:
                    return password
                raise forms.ValidationError('wrong password')
            raise forms.ValidationError("user dose'nt exist")