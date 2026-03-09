from django.db import models


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('pizza', 'Pizza'),
        ('sides', 'Sides'),
        ('drinks', 'Drinks'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='pizza')

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('sent', 'Sent to Kitchen'),
        ('done', 'Done'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    table_number = models.CharField(max_length=20, blank=True, default='Walk-in')
    notes = models.TextField(blank=True)
    rush = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} — {self.status}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    def subtotal(self):
        return self.menu_item.price * self.quantity