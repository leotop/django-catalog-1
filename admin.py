# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from models import Category, Manufacturer, Product, ProductImages, ProductAttribute
from mptt.admin import MPTTModelAdmin
#from ckeditor.widgets import CKEditorWidget
from django_mptt_admin.admin import DjangoMpttAdmin

# ACTIONS
def move_to_category(modeladmin, request, queryset):
       form = None

       if 'apply' in request.POST:
           form = ChangeCategoryForm(request.POST)

           if form.is_valid():
               category = form.cleaned_data['category']

               count = 0
               for item in queryset:
                   item.category = category
                   item.save()
                   count += 1

               modeladmin.message_user(request, "Категория %s применена к %d товарам." % (category, count))
               return HttpResponseRedirect(request.get_full_path())

       if not form:
           form = ChangeCategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

       return render(request, 'catalog/move_to_category.html', {'items': queryset,'form': form, 'title':u'Изменение категории'})

def move_to_manufacturer(modeladmin, request, queryset):
       form = None

       if 'apply' in request.POST:
           form = ChangeManufacturerForm(request.POST)

           if form.is_valid():
               manufacturer = form.cleaned_data['manufacturer']

               count = 0
               for item in queryset:
                   item.manufacturer = manufacturer
                   item.save()
                   count += 1

               modeladmin.message_user(request, "Производитель %s применена к %d товарам." % (manufacturer, count))
               return HttpResponseRedirect(request.get_full_path())

       if not form:
           form = ChangeManufacturerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

       return render(request, 'catalog/move_to_manufacturer.html', {'items': queryset,'form': form, 'title':u'Изменение производителя'})

move_to_manufacturer.short_description = u"Изменить производителя"
move_to_category.short_description = u"Изменить категорию"

# FORMS
class ChangeCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label=u'Основная категория')

class ChangeManufacturerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), label=u'Новый производитель')

class ProductAdminForm(forms.ModelForm):
    #description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product

class ManufacturerAdminForm(forms.ModelForm):
    #description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Manufacturer

class CategoryAdminForm(forms.ModelForm):
    #description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Category


# ADMIN
class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 0

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'manufacturer', 'on_demand',)
    list_filter = ['on_demand', 'manufacturer', 'category']
    fieldsets = (
        (None, {'fields': (
            'name',
            'price',
            'manufacturer',
            'category',
            'on_demand',
            'description',
        )}),
    )

    inlines = [ProductImageInline, ProductAttributeInline, ]
    ordering = [ 'name', 'price', 'manufacturer', ]
    form = ProductAdminForm
    actions = [move_to_category, move_to_manufacturer]

class ManufacturerAdmin(admin.ModelAdmin):
    readonly_fields = ['product_list']
    list_display = ('name', 'product_count',)
    ordering = ['name', ]
    form = ManufacturerAdminForm

#admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Category, DjangoMpttAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Product, ProductAdmin)
