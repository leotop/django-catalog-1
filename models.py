# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(_('Name'), max_length = 127)
    image = models.ImageField(_(u'Image'), blank=True, null=True, upload_to="catalog/category/")
    description = models.TextField(_(u'Description'), blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def get_absolute_url(self):
        return '/category/%d/' % self.id

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

class Manufacturer(models.Model):
    name = models.CharField(_(u'Name'), max_length = 127)
    image = models.ImageField(_(u'Image'), blank=True, null=True, default=None, upload_to="catalog/manufacturer/")
    description = models.TextField(_(u'Description'), blank=True, null=True, default=None)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        model_name = self.__class__.__name__.lower()
        return '/%s/%d/' % (model_name, self.id)

    class Meta:
        abstract = True
        verbose_name = _(u'Manufacturer')
        verbose_name_plural = _(u'Manufacturers')

class Product(models.Model):
    name = models.CharField(_(u'Name'), max_length = 127)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    price = models.IntegerField(_(u'Price'), default=0)
    category = models.ForeignKey(Category, verbose_name=_(u'Category'))
    active = models.BooleanField(default=True)
    #manufacturer = models.ForeignKey(Manufacturer, verbose_name=_(u'Manufacturer'))
    #on_demand = models.BooleanField(_(u'On Demand'), default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        model_name = self.__class__.__name__.lower()
        return '/%s/%d/' % (model_name, self.id)

    def get_images(self):
        return ProductImages.objects.filter(product_id=self.id)

    def get_primary_image(self):
        return self.get_images()[0]

    class Meta:
        abstract = True
        verbose_name = _(u'Product')
        verbose_name_plural = _(u'Products')

