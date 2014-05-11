# -*- coding: utf-8 -*-

from django import template
from ..models import *

# Регистрируем новую библиотеку тегов
register = template.Library()

@register.inclusion_tag('catalog/cat_tree.html', takes_context=True)
def category_tree(context, cat_id=0):
    context['nodes'] = Category.objects.all()

    # full path to current category
    if cat_id:
        curnode = Category.objects.get(id=cat_id)
        context['current_nodes'] = list(curnode.get_ancestors())
        context['current_nodes'].append(curnode)
    else:
        context['current_nodes'] = []

    return context

