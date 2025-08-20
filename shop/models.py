from django.db import models
from decimal import Decimal
from django.db.models import Q, F, Sum
from django.core.validators import MinValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    description = models.TextField(blank=True, default="")
    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)

    def __str__(self):
        return self.name
    

class Order(TimeStampedModel):
    products = models.ManyToManyField(Product, through='OrderProduct', related_name='orders')

    class Meta:
        ordering = ("-created_at",)

    @property
    def item_count(self) -> int:
        agg = self.order_items.aggregate(total=Sum("quantity"))
        return agg["total"] or 0

    @property
    def total_price(self) -> Decimal:
        agg = self.order_items.aggregate(
            total=Sum(F("quantity") * F("unit_price"))
        )
        return agg["total"] or Decimal("0.00")
    
    def __str__(self):
        return f"Order #{self.id}"
    

class OrderProduct(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order","product"], name="unique_order_product"),
            models.CheckConstraint(check=Q(quantity__gt=0), name="orderproduct_quantity_gt_0"),
        ]
    
    def save(self, *args, **kwargs):
        if self.unit_price in (None, ""):
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} * {self.product.name} @ {self.unit_price} in Order #{self.order.id}'
    

class Cart(TimeStampedModel):
    products = models.ManyToManyField(Product, through='CartProduct', related_name='carts', blank=True)

    class Meta:
        ordering = ("-created_at",)

    @property
    def item_count(self) -> int:
        agg = self.cart_items.aggregate(total=Sum("quantity"))
        return agg["total"] or 0

    @property
    def total_price(self) -> Decimal:
        agg = self.cart_items.aggregate(
            total=Sum(F("quantity") * F("product__price"))
        )
        return agg["total"] or Decimal("0.00")
    
    def __str__(self):
        return f'Cart #{self.id}'
    

class CartProduct(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart","product"], name="unique_cart_product"),
            models.CheckConstraint(check=Q(quantity__gt=0), name="cartproduct_quantity_gt_0"),
        ]
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Cart {self.cart.id}'