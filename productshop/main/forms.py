from django import forms
from . models import Product, Order
from phonenumber_field.modelfields import PhoneNumberField


MIN_RESOLUTION = (700, 500)


class CreateProductForm(forms.ModelForm):

    title = forms.CharField(label='Заголовок', max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Описание', max_length=120,
                              widget=forms.TextInput(attrs={'rows': 4, 'cols': 15}))
    price = forms.DecimalField(label='Цена', max_digits=10, decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    img = forms.ImageField()

    class Meta:
        model = Product
        fields = ('title', 'cat', 'img', 'price', 'content',)


class OrderForm(forms.ModelForm):

    phone = PhoneNumberField(null=False, blank=False, unique=True)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type', 'comment')