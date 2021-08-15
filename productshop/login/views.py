from django.contrib.auth import logout
from django.contrib.auth.models import User
from main.models import Product, Order
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .forms import RegisterUserForm, LoginUserForm
from main.mixins import DetailBarMixin, ListBarMixin, TemplateBarMixin


bar_left = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Про нас', 'url_name': 'about'},
]


class LoginUser(TemplateBarMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class RegisterUser(DetailBarMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('login')


class ResetUserPasswordView(TemplateBarMixin, PasswordResetView):
    template_name = 'login/password-reset-form.html'


