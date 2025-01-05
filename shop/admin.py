from django.contrib import admin
from .models import Product, Category, Cart, Order, OrderProduct, CartProduct, Wishlist, WishlistProduct

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Wishlist)
admin.site.register(WishlistProduct)
