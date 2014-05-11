# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import generic_categories, show_category, show_product, show_manufacturer
#from django.views.generic import DetailView, ListView
#from models import Manufacturer

urlpatterns = patterns('',
    url(r'^$', 'catalog.views.generic_categories'),
    url(r'^category/(?P<pk>\d+)/$', 'catalog.views.show_category'),
    url(r'^category/(?P<pk>\d+)/page(?P<page>\d+)$', 'catalog.views.show_category'),
    url(r'^product/(?P<prod_id>.*)/$', 'catalog.views.show_product'),
    url(r'^manufacturer/(?P<pk>\d+)/$', 'catalog.views.show_manufacturer'),
)

