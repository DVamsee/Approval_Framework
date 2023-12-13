from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from .models import User_profile,Comment,Company,Workflow


User = get_user_model()

class CompanyForm(forms.Form):
    name = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'name',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'First Name' ,

            }
        )
    )
    place = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'place',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'First Name' ,

            }
        )
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        obj = Company.objects.filter(name = name).first()
        if obj:
            raise forms.ValidationError("company profile already exist")
        return name
    
class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'first_name',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'First Name' ,

            }
        )
    )
    last_name = forms.CharField(
        max_length=20,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'last_name',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'Last Name' ,

            }
        )
    )
    email = forms.EmailField(
        max_length = 30,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'last_name',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'example@gmail.com' ,

            }
        )
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
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
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
    email = forms.EmailField(
    widget= forms.TextInput(
            attrs={
                'id': 'email',
                'placeholder' : 'email' ,
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                
            }
        )
    )

    password = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'type':'password',
                'id': 'password',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 10*'x' ,

            }
        )
    )

    def clean_username(self):
        email = self.cleaned_data.get('email')
        obj_username = User.objects.filter(username = email )
        if obj_username:
            return email
        raise forms.ValidationError("username does'nt exist")
    
    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        obj = User.objects.filter(username = email).first()
        if obj:
            user = User_profile.objects.filter(User = obj.id, password = password)
            if user!=None:
                return password
            raise forms.ValidationError('wrong password')
        raise forms.ValidationError("user dose'nt exist")
    


class WorkflowForm(forms.Form):
    name = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'name',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'Name' ,

            }
        )
    )
    description = forms.CharField(
    max_length = 100,
    widget = forms.Textarea(
        attrs={
            'type':'text',
            'id': 'name',
            'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            'placeholder' : 'Description' ,

        }
    )
    )
    threshold_value = forms.CharField(
        widget = forms.TextInput(
        attrs={
            'type':'text',
            'id': 'threshold_value',
            'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            'placeholder' : 'value > 100' ,

        }
    )
    )
    def __init__(self, *args, **kwargs):
        super(WorkflowForm, self).__init__(*args, **kwargs)

        # Dynamically retrieve staff users and generate choices
        staff_users = User_profile.objects.filter(role='staff')
        staffs = dict()
        for user in staff_users:
            staffs[user.id] = user.User.first_name
        choices = tuple(list((i,i) for i in range(1,len(staff_users)+1)))
        # Create a MultipleChoiceField with dynamic choices
        for id in staffs.keys():

            self.fields[staffs[id]] = forms.ChoiceField(
                choices=choices,
                required=True,  # You can set it to True if at least one staff user is required
            )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        workflow = Workflow.objects.filter(name=name)
        if workflow:
            raise forms.ValidationError("Workflow with this name already exists")
        return name

    def clean_threshold_value(self):
        number = self.cleaned_data.get('threshold_value')
        workflow = Workflow.objects.filter(threshold_value=number)

        if not workflow:
            if int(number)>100:
                return number
            raise forms.ValidationError('enter threshold frequency greater than 100')
        raise forms.ValidationError('Workflow with this threshold already exist')
    

class ApprovalForm(forms.Form):
    header_detail = forms.CharField(
        max_length=100,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'header_detail',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'Approval heading' ,

            }
        )
    )
    line_item_detail = forms.CharField(
        max_length=100,
        widget = forms.TextInput(
            attrs={
                'type':'text',
                'id': 'line_item_detail',
                'class' : 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
                'placeholder' : 'description about approval' ,

            }
        )
    )
    aproval_choices = (
        ('urgent','urgent'),
        ('small','small'),
        ('adhoc','adhoc'),
    )
    approval_type = forms.ChoiceField(
        choices = aproval_choices,
    )

