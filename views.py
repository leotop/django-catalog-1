# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from models import Product, Category, Manufacturer, ProductImages, ProductAttribute

def generic_categories(request):
    gcat = Category.objects.filter(parent_id=None)
    cat = {'name': u"Основные категории", 'description': u""}
    return render_to_response("catalog/category.html", {
        'category': cat,
        'subcategories': gcat,
    })

def show_category(request, pk, page=1):
    try:
        c = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        raise Http404

    subcategories = Category.objects.filter(parent=c)

    order_list = ['manufacturer__name', '-manufacturer__name', 'price', '-price']

    order = request.GET.get('order')

    order1 = order
    if order not in order_list:
        order1 = 'manufacturer__name'

    products = Product.objects.filter(category=c).order_by(order1)

    # Pagination
    paginator = Paginator(products, 10)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render_to_response('catalog/category.html', {
        'category': c,
        'products': products,
        'subcategories': subcategories,
        'queries': request.GET.urlencode,
        })

def show_product(request, prod_id):
    from re import sub

    try:
        p = Product.objects.get(id=prod_id)
        pa = ProductAttribute.objects.filter(product_id=prod_id).exclude(name="markertoys_id")
        pa = pa.exclude(name=u'цена из прайса')
        pmi = p.get_images()
    except Product.DoesNotExist:
        raise Http404

    editable = False
    if request.user.is_authenticated():
        editable = True

    return render_to_response('catalog/product_details.html', {
        'p': p,
        'pa': pa,
        'pmi': pmi,
        'editable': editable
    })

def show_manufacturer(request, pk):

    products = Product.objects.filter(manufacturer_id=pk)

    # Pagination
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    editable = False
    if request.user.is_authenticated():
        editable = True

    return render_to_response('catalog/manufacturer.html', {
        'manufacturer': get_object_or_404(Manufacturer, pk=pk),
        'products': products,
        'editable': editable,
    })
