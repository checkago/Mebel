# Generated by Django 4.1.1 on 2022-09-15 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.uploading


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('metro', models.CharField(blank=True, max_length=50, null=True, verbose_name='ст. Метро')),
                ('street', models.CharField(max_length=300, verbose_name='Улица, дом, квартира, подъезд')),
                ('building', models.CharField(max_length=7, verbose_name='Дом')),
                ('apartment', models.CharField(blank=True, max_length=5, null=True, verbose_name='Квартира')),
                ('entrance', models.CharField(blank=True, max_length=2, null=True, verbose_name='Подъезд')),
                ('primary', models.BooleanField(default=True, verbose_name='Основной адрес?')),
            ],
            options={
                'verbose_name': 'Адрес покупателя',
                'verbose_name_plural': 'Адреса покупателей',
            },
        ),
        migrations.CreateModel(
            name='Baner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('info', models.CharField(max_length=100, verbose_name='Информация')),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function, verbose_name='Изображение')),
                ('link', models.URLField(blank=True, null=True, verbose_name='ссылка')),
            ],
            options={
                'verbose_name': 'Банер',
                'verbose_name_plural': 'Банеры',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.IntegerField(default=0, verbose_name='Общее кол-во товаров в корзине')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True, verbose_name='Общая стоимость')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины покупателей',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним/Slug')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('phone', models.CharField(max_length=18, verbose_name='Номер телефона')),
                ('agreement', models.BooleanField(default=False, verbose_name='Согласен с обработкой п.д.')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('user_addresses', models.ManyToManyField(blank=True, related_name='addresses', to='magazin.address', verbose_name='Адрес покупателя')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Список покупателей',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=18, verbose_name='Номер телефона')),
                ('status', models.CharField(choices=[('Новый', 'Новый заказ'), ('Подтвержден', 'Заказ подтвержден'), ('В работе', 'Заказ в обработке'), ('Готов', 'Заказ готов'), ('Получен', 'Заказ получен'), ('Отменен', 'Заказ отменен')], default='Новый', max_length=100)),
                ('buying_type', models.CharField(blank=True, choices=[('Доставка', 'Доставка'), ('Самовывоз из магазина', 'Самовывоз из магазина')], default='Доставка', max_length=100, null=True, verbose_name='Тип покупки')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateField(auto_now=True, verbose_name='дата создания заказа')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='magazin.address', verbose_name='Адрес')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='magazin.cart', verbose_name='Корзина')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='magazin.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказ покупателя',
                'verbose_name_plural': 'Заказы покупателей',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним/Slug')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('description', models.TextField(default='Описание товара появится позже', verbose_name='Описание товара')),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function)),
                ('use_in_slider', models.BooleanField(default=False, verbose_name='Использовать в слайдере')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Галерея изображений',
                'verbose_name_plural': 'Галерея изображений',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='user_orders',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='magazin.order', verbose_name='Заказы покупателя'),
        ),
        migrations.AddField(
            model_name='customer',
            name='wishlist',
            field=models.ManyToManyField(blank=True, to='magazin.item', verbose_name='Лист ожидания'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая стоимость')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.cart', verbose_name='Корзина')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='magazin.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Продукт корзины',
                'verbose_name_plural': 'Продукты корзины',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='magazin.customer', verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='magazin.cartproduct', verbose_name='Товары в корзине'),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='magazin.customer', verbose_name='Покупатель'),
        ),
    ]
