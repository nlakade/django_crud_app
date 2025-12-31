from django.db import models
from django.utils import timezone

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('CLOTHING', 'Clothing'),
        ('BOOKS', 'Books'),
        ('HOME', 'Home & Garden'),
        ('SPORTS', 'Sports'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='OTHER')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (${self.price})"
    
    class Meta:
        ordering = ['-created_at']