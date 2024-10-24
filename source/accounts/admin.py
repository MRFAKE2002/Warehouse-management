from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BaseUser
from .forms import BaseUserCreationForm, BaseUserChangeForm


@admin.register(BaseUser)
class CustomAdmin(UserAdmin):
    model = BaseUser

    add_form = BaseUserCreationForm

    form = BaseUserChangeForm

    list_display = ['username', 'email',]

