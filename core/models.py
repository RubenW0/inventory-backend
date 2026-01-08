from django.db import models
from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class ProductStatus(Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"

    @classmethod
    def choices(cls):
        return [(status.value, status.value.replace("_", " ").title()) for status in cls]



class Product(models.Model):
    name = models.CharField(max_length=100, default="")  # default string, niet 0
    type = models.CharField(max_length=50, default="")   # default string
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    min_stock = models.PositiveIntegerField(default=0)
    advised_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    location = models.CharField(max_length=50, default="")
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices(),
        default=ProductStatus.IN_STOCK.value
    )

    def __str__(self):
        return f"{self.name} ({self.type})"

class Supplier(models.Model):
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=150, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name

class OrderStatus(Enum):
    PENDING = "pending"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return [(s.value, s.value.replace("_", " ").title()) for s in cls]

class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices(),
        default=OrderStatus.PENDING.value
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)   # linkt met jouw bestaande Product
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role="employee"):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password, role="admin")
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("employee", "Employee"),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username
