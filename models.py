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
        return '/manufacturer/%d/' % self.id

    def product_list(self):
        from django.core import urlresolvers
        p = u''
        for i in Product.objects.filter(manufacturer=self):
            admin_url = urlresolvers.reverse(
                "admin:catalog_product_change", args=[i.id]
            )
            p += u'<a href="%s">(edit) - </a>%s<br>' % (admin_url, i.name)

        return p

    product_list.short_description = u'Товары'
    product_list.allow_tags = True

    def product_count(self):
        return Product.objects.filter(manufacturer=self).count()

    product_count.admin_order_field = 'product_count'

    class Meta:
        verbose_name = _(u'Manufacturer')
        verbose_name_plural = _(u'Manufacturers')

class Product(models.Model):
    name = models.CharField(_(u'Name'), max_length = 127)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    price = models.IntegerField(_(u'Price'), default=0)
    category = models.ForeignKey(Category, verbose_name=_(u'Category'))
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_(u'Manufacturer'))
    on_demand = models.BooleanField(_(u'On Demand'), default=False)

    def __unicode__(self):
        return self.name

    def get_markertoys_id(self):
        try:
            pa = ProductAttribute.objects.get(product_id=self.id, name="markertoys_id")
            return pa.value
        except ProductAttribute.DoesNotExist:
            return ''

    def get_images(self):
        return ProductImages.objects.filter(product_id=self.id)

    def get_primary_image(self):
        from PIL import Image, ImageEnhance
        from django.conf import settings
        from django.core.files import File
        import os

        try:
            img = ProductImages.objects.filter(product_id=self.id)[0]
        except IndexError:
            return 0

        img = img.image
        image = Image.open( settings.MEDIA_ROOT + "/" + img.name )
        watermark = Image.open(settings.STATIC_ROOT + '/logo_text.png')
        opacity = 1

        imagename = "%s.wm.jpg" % img.name
        if os.path.isfile(imagename):
            return imagename

        assert opacity >= 0 and opacity <= 1
        if opacity < 1:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            else:
                watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)

        layer = Image.new('RGBA', image.size, (0,0,0,0))
        layer.paste(watermark, (15, image.size[1]-45))

        i = Image.composite(layer,  image,  layer)
        #imagename = "%s.wm.jpg" % img.name
        i.save(settings.MEDIA_ROOT + "/" + imagename)

        return imagename

    def get_absolute_url(self):
        return '/product/%d/' % self.id

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Product')
        verbose_name_plural = _(u'Products')

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(_(u'Image'), blank=True, default=None, null=True, upload_to="catalog/product/")

    class Meta:
        verbose_name = _(u'Product image')
        verbose_name_plural = _(u'Product images')

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attribute')
    name = models.CharField(max_length=127)
    value = models.CharField(max_length=255)

