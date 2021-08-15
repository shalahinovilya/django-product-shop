from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

user= get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Электронная почта',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = user
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if user.objects.filter(email__iexact=email).count():
            raise ValidationError('Учетная запись с такой электронной почтой уже существует')
        return email


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(label='Логин', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-login-field'}))
    password = forms.CharField(label='Пароль', max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-login-field'}))

    class Meta:
        model = user
        fields = ('username', 'password')