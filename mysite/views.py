from django.shortcuts import render
from django.template import loader
#from . import templates
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request,'acceuil.html' )


from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    return value.as_widget(attrs={'class': f'{css_classes} {arg}'})