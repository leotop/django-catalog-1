# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import generic_categories, show_category, show_product, show_manufacturer
#from django.views.generic import DetailView, ListView
#from models import Manufacturer

urlpatterns = patterns('',
    url(r'^$', generic_categories),
    url(r'^category/(?P<pk>\d+)/$', show_category),
    url(r'^category/(?P<pk>\d+)/page(?P<page>\d+)$', show_category),
    url(r'^product/(?P<prod_id>.*)/$', show_product),
    url(r'^manufacturer/(?P<pk>\d+)/$', show_manufacturer),
)

