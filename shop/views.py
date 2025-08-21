from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, ProductImage
from django.db.models import Prefetch


class IndexView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.order_by("-is_main", "created_at", "id"))
        )
        context['products'] = products
        return context
    

class ProductDetailView(TemplateView):
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=kwargs['pk'])
        return context
