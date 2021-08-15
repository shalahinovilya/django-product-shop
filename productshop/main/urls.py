from django.urls import path
from . views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('add-product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<slug:product_slug>/', ProductDetailView.as_view(), name='product'),
    path('product/<slug:product_slug>/update-product/', UpdateProductView.as_view(), name='update_product'),
    path('product/<slug:product_slug>/delete-product/', DeleteProductView.as_view(), name='delete_product'),
    path('cabinet/',  CabinetView.as_view(), name='cabinet'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/<int:id>/', AddToCartView.as_view(), name='add_cart'),
    path('delete-from-cart/<int:id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/<int:id>/', ChangeQTY.as_view(), name='change_qty'),
    path('cabinet/user-posts/', UserPostsView.as_view(), name='user_posts'),
    path('check-order/', CheckOrderView.as_view(), name='check_order'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('cabinet/user-orders/', UserOrdersView.as_view(), name='user_orders'),
]