# shop/models.py
from django.db import models
from django.contrib.auth.models import User  # <-- ADD THIS IMPORT

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, help_text="Comma-separated values (e.g., 'electronics,laptop,gaming')")

    def __str__(self):
        return self.name

    def get_tags_list(self):
        return [tag.strip().lower() for tag in self.tags.split(',') if tag.strip()]

# --- ADD ALL THE CODE BELOW ---

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Don't delete product if in an order
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

class UserFeedback(models.Model):
    LIKE = 1
    DISLIKE = -1
    FEEDBACK_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feedback = models.IntegerField(choices=FEEDBACK_CHOICES)

    class Meta:
        # Ensures a user can only give one feedback per product
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.get_feedback_display()}"