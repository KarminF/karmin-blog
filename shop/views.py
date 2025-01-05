from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product

class IndexView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
    

class ProductDetailView(TemplateView):
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=kwargs['pk'])
        return context