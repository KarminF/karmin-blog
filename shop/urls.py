from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]