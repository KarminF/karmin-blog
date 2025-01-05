from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} with {self.quantity} items"
    
    def save(self, *args, **kwargs):
        self.quantity = self.quantity = sum(item.quantity for item in self.orderproduct_set.all())
        self.total_price = sum(item.product.price * item.quantity for item in self.orderproduct_set.all())
        super().save(*args, **kwargs)
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'
    

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')
    # quantity of defferent products
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id}'
    
    def save(self, *args, **kwargs):
        self.quantity = sum(item.quantity for item in self.cartproduct_set.all())
        self.total_price = sum(item.product.price * item.quantity for item in self.cartproduct_set.all())
        super().save(*args, **kwargs)
    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Cart {self.cart.id}'
    

class Wishlist(models.Model):
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist {self.id}'
    

class WishlistProduct(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} in Wishlist {self.wishlist.id}'