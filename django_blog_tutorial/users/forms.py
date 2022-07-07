from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class MyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        print(self.helper)
        # self.helper.form_class = 'form-horizontal'
        self.helper.template = 'users/form_template.html'
        # self.helper.field_template = 'users/field.html'
        self.helper.layout = Layout(
            Field('username', template='users/field.html'),
            Field('password', template='users/field.html')
            # Submit('login', 'Sign in')
        )



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
