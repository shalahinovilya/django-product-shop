from datetime import datetime
from django_resized import ResizedImageField
from decimal import Decimal
import transliterate
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from PIL import Image
user = get_user_model()


class Category(models.Model):

    name = models.CharField(verbose_name='Имя категории', max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


MIN_RESOLUTION = (500, 700)


def valid_size(photo):
    if photo:
        img = photo
        image = Image.open(img)
        min_height, min_width = MIN_RESOLUTION
        if image.height < min_height or image.width < min_width:
            raise ValidationError(f'Размер изображение не должен быть меньше {MIN_RESOLUTION[0]}x{MIN_RESOLUTION[1]}')


class Product(models.Model):

    title = models.CharField(verbose_name='Заголовок', max_length=50)
    cat = models.ForeignKey(Category, verbose_name='Вид продукта', on_delete=models.PROTECT)
    content = models.TextField(verbose_name='Описание продукта', max_length=255)
    img = ResizedImageField(size=[MIN_RESOLUTION[1], MIN_RESOLUTION[0]], quality=95, crop=['middle', 'center'], upload_to='photos', verbose_name='Фото', validators=[valid_size])
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0,
                                validators=[MinValueValidator(Decimal('0'))], help_text='Введите цену в долларах')
    slug = AutoSlugField(null=True, default=None, always_update=True, unique=True, db_index=True, verbose_name='URL',
                         populate_from='title')
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    create_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='Время последнего изменения', auto_now=True)

    def save(self, *args, **kwargs):
        # self.slug = transliterate.translit(str(self.title).lower(), reversed=True)
        # photo = Image.open(self.img.path)
        # if photo.height > MIN_RESOLUTION[0] or photo.width > MIN_RESOLUTION[0]:
        #     photo.thumbnail(MIN_RESOLUTION, Image.ANTIALIAS)

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['create_time']


class Cart(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True, verbose_name='Владелец')
    products = models.ManyToManyField('CartProduct', blank=True, related_name='cart_products')
    for_anonymous = models.BooleanField(default=False)
    number_of_items = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0,
                                      verbose_name='Общая цена', null=True, blank=True)
    in_order = models.BooleanField(default=False)


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, verbose_name='Продукты корзины')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая цена')

    def save(self, *args, **kwargs):
        self.final_price = int(self.qty) * int(self.product.price)
        return super().save(*args, **kwargs)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_SELF = 'self'
    BUYING_DELIVERY = 'delivery'

    BUYING_CHOICES = (
        (BUYING_SELF, 'Самовывоз'),
        (BUYING_DELIVERY, 'Доставка')
    )

    user = models.ForeignKey(user, verbose_name='Покупатель', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    address = models.CharField(max_length=150, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина заказа', null=True)
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_CHOICES, default=BUYING_DELIVERY)
    comment = models.TextField(max_length=254, verbose_name='Комментарий', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='Дата создания заказа', auto_now_add=True)

    def __str__(self):
        return str(self.id)
