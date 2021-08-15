# Generated by Django 3.2.3 on 2021-08-10 08:54

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_anonymous', models.BooleanField(default=False)),
                ('number_of_items', models.PositiveIntegerField(default=0, verbose_name='Количество товара')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Общая цена')),
                ('in_order', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Имя категории')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('content', models.TextField(max_length=255, verbose_name='Описание продукта')),
                ('img', models.ImageField(upload_to='photos')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, default=None, editable=False, null=True, populate_from='title', unique=True, verbose_name='URL')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.category', verbose_name='Вид продукта')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['create_time'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('ready', 'Заказ готов'), ('completed', 'Заказ выполнен')], default='new', max_length=100, verbose_name='Статус заказа')),
                ('buying_type', models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='delivery', max_length=100, verbose_name='Тип заказа')),
                ('comment', models.TextField(blank=True, max_length=254, null=True, verbose_name='Комментарий')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cart', verbose_name='Корзина заказа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая цена')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product', verbose_name='Продукты корзины')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='cart_products', to='main.CartProduct'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]