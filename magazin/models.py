from django.urls import reverse
from django.conf import settings
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import operator
from django.db import models
from utils import upload_function
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Псевдоним/Slug')

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


class ImageGallery(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)



    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Изображение для {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="100px"')


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Псевдоним/Slug')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.CharField(max_length=12, verbose_name='Цена')
    description = models.TextField(default='Описание товара появится позже', verbose_name='Описание товара')
    image_gallery = GenericRelation('imagegallery')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} | {self.category.name}"

    @property
    def ct_model(self):
        return self._meta.model_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'brand_slug': self.brand.slug,
                                                 'product_slug': self.slug})


class CartProduct(models.Model):

    MODEL_CARTPRODUCT_DISPLAY_NAME_MAP = {
        "Product": {"is_constructable": True, "fields": ['name', 'brand.name'], "separator": '-'}
    }

    user = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'

    @property
    def display_name(self):
        model_fields = self.MODEL_CARTPRODUCT_DISPLAY_NAME_MAP.get(self.content_object.__class__._meta.model_name.capitalizer())
        if model_fields and model_fields['is_constructable']:
            display_name = model_fields['separator'].join(
                [operator.attrgetter(fied)(self.content_object) for fied in model_fields['fields']]
            )
            return display_name
        if model_fields and not model_fields['is_constructable']:
            display_name = operator.attrgetter(model_fields['field'])

    def __str__(self):
        return f"Продукт: {self.content_object} для корзины"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Покупатель')
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart',
                                      verbose_name='Товары в корзине')
    total_products = models.IntegerField(default=0, verbose_name='Общее кол-во товаров в корзине')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Общая стоимость',
                                      null=True, blank=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины покупателей'

    def __str__(self):
        return f"Корзина №{self.id} | Пользователь -  {self.owner}"


class Order(models.Model):

    STATUS_NEW = 'Новый'
    STATUS_CONFIRMED = 'Подтвержден'
    STATUS_IN_PROGRESS = 'В работе'
    STATUS_READY = 'Готов'
    STATUS_COMPLETED = 'Получен'
    STATUS_CANCELLED = 'Отменен'

    BYING_TYPE_SELF = 'Самовывоз из магазина'
    BYING_TYPE_DELIVERY = 'Доставка'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_CONFIRMED, 'Заказ подтвержден'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ получен'),
        (STATUS_CANCELLED, 'Заказ отменен')
    )

    BYING_TYPE_CHOICES = (
        (BYING_TYPE_DELIVERY, 'Доставка'),
        (BYING_TYPE_SELF, 'Самовывоз из магазина')
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders', verbose_name='Покупатель')
    address = models.ForeignKey('Address', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Адрес')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='Корзина')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, blank=True, null=True,
                                   choices=BYING_TYPE_CHOICES,
                                   default=BYING_TYPE_DELIVERY, verbose_name='Тип покупки')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')
    created_at = models.DateField(auto_now=True, verbose_name='дата создания заказа')

    class Meta:
        verbose_name = 'Заказ покупателя'
        verbose_name_plural = 'Заказы покупателей'

    def __str__(self):
        return f"MS-000{self.id}"


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    user_addresses = models.ManyToManyField('Address', blank=True, related_name='addresses', verbose_name='Адрес покупателя')
    user_orders = models.ManyToManyField(Order, blank=True, related_name='related_customer', verbose_name='Заказы покупателя')
    wishlist = models.ManyToManyField(Item, blank=True, verbose_name='Лист ожидания')
    agreement = models.BooleanField(default=False, verbose_name='Согласен с обработкой п.д.')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Список покупателей'

    def __str__(self):

        return f"{self.user.username}"


class Address(models.Model):
    customer = models.ForeignKey('Customer', related_name="addresses", on_delete=models.CASCADE, verbose_name='Покупатель')
    city = models.CharField(max_length=50, verbose_name='Город')
    metro = models.CharField(max_length=50, blank=True, null=True, verbose_name='ст. Метро')
    street = models.CharField(max_length=300, verbose_name='Улица, дом, квартира, подъезд')
    building = models.CharField(max_length=7, verbose_name='Дом')
    apartment = models.CharField(max_length=5, blank=True, null=True, verbose_name='Квартира')
    entrance = models.CharField(max_length=2, blank=True, null=True, verbose_name='Подъезд')
    primary = models.BooleanField(default=True, verbose_name='Основной адрес?')

    class Meta:
        verbose_name = 'Адрес покупателя'
        verbose_name_plural = 'Адреса покупателей'

    def __str__(self):
        return f"{self.city}, {self.metro}, {self.street}, {self.street}, {self.building}"


class Baner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    info = models.CharField(max_length=100, verbose_name='Информация')
    image = models.ImageField(upload_to=upload_function, verbose_name='Изображение')
    link = models.URLField(verbose_name='ссылка', blank=True, null=True)

    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банеры'

    def __str__(self):
        return self.name

