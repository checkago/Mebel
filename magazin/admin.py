from django.contrib import admin
from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from magazin.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ItemAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Item
        fields = '__all__'


class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    readonly_fields = ('image_url',)


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageGalleryInline]
    form = ItemAdminForm
    list_display = ('name', 'category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(ImageGallery)
admin.site.register(Baner)

