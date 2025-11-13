from django.db import models

# Create your models here.
from django.db import models
from enum import Enum

class ProductStatus(Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"

    @classmethod
    def choices(cls):
        return [(status.value, status.name.replace("_", " ").title()) for status in cls]

class Product(models.Model):
    name = models.CharField(max_length=100, default=0)
    type = models.CharField(max_length=50, default=0)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_stock = models.PositiveIntegerField(default=0)
    advised_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=50, default=0)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices(),
        default=ProductStatus.IN_STOCK.value
    )

    def __str__(self):
        return f"{self.name} ({self.type})"
