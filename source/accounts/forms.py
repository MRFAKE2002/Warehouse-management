from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

class BaseUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class BaseUserChangeForm(UserChangeForm):

    class Meta:

        model = get_user_model()
        fields = ('username', 'email')
