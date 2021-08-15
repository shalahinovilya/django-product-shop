from django import template
from django.db import models


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data.get('final_price__sum')
    else:
        cart.final_price = 0
    cart.number_of_auto = cart_data.get('id__count')
    cart.save()