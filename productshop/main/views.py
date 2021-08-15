from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,  TemplateView, DeleteView, View, CreateView, UpdateView
from . models import Product, Cart, CartProduct, Order
from . mixins import *
from . utils import *
from . forms import OrderForm

bar_left = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Про нас', 'url_name': 'about'},
]


class HomeView(ListBarMixin, ListView):
    paginate_by = 4
    template_name = 'main/index.html'
    context_object_name = 'products'
    model = Product


class ProductDetailView(DetailBarMixin, DetailView):
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    template_name = 'main/product_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context


class AboutTemplateView(TemplateBarMixin, TemplateView):
    template_name = 'main/about.html'


class ContactTemplateView(TemplateBarMixin, TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context


class CabinetView(TemplateView):
    template_name = 'main/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context


class ProductCreateView(DetailBarMixin, LoginRequiredMixin, CreateView):
    model = Product
    slug_url_kwarg = 'post_slug'
    template_name = 'main/add_product.html'
    success_url = reverse_lazy('home')
    fields = ('title', 'cat', 'img', 'price', 'content')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return HttpResponseRedirect('/')


class UpdateProductView(DetailBarMixin, UpdateView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'main/update_product.html'
    success_url = reverse_lazy('home')
    fields = ('title', 'cat', 'img', 'price', 'content')


class DeleteProductView(DeleteView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'main/delete_product.html'
    success_url = reverse_lazy('home')


class CartView(DetailBarMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        cart, cart_created = Cart.objects.get_or_create(user=request.user, in_order=False)
        cart_items = cart.products.all()
        context = {
             'cart_items': cart_items,
             'bar_left': bar_left,
             'cart': cart
         }
        return render(request, 'main/cart.html', context)


class AddToCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        cart, cart_created = Cart.objects.get_or_create(user=request.user, in_order=False)
        product = Product.objects.get(id=kwargs.get('id'), slug=kwargs.get('slug'))
        cart_item, cart_item_created = CartProduct.objects.get_or_create(product=product, cart=cart)
        if cart_item_created:
            cart.products.add(cart_item)
        recalc_cart(cart)
        return HttpResponse(status=204)


class DeleteFromCartView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=kwargs.get('id'))
        cart_item = CartProduct.objects.get(product=product, cart=cart)
        cart.products.remove(cart_item)
        cart_item.delete()
        recalc_cart(cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTY(View):

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user, in_order=False)
        product = Product.objects.get(id=kwargs.get('id'))
        cart_item = CartProduct.objects.get(product=product, cart=cart)
        new_qty = request.POST.get('qty')
        cart_item.qty = new_qty
        cart_item.save()
        recalc_cart(cart)
        return HttpResponseRedirect('/cart/')


class UserPostsView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'products': Product.objects.filter(created_by=request.user),
            'bar_left': bar_left
        }

        return render(request, 'main/user_posts.html', context)


class UserOrdersView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'orders': Order.objects.filter(user=request.user),
            'bar_left': bar_left
        }

        return render(request, 'main/user_orders.html', context)


class CheckOrderView(DetailBarMixin, View):

    def get(self, request, *args, **kwargs):
        cart, cart_created = Cart.objects.get_or_create(user=request.user, in_order=False)
        cart_items = cart.products.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart_items': cart_items,
            'bar_left': bar_left,
            'form': form
        }
        return render(request, 'main/check_order.html', context)


class MakeOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart.objects.get(user=request.user, in_order=False)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.comment = form.cleaned_data['comment']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.save()
            cart.in_order = True
            cart.save()
            new_order.cart = cart
            new_order.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/check-order/')
