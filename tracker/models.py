from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_income = models.BooleanField(default=False)  # True — дохід, False — витрата
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )

    def __str__(self):
        return f"{self.name} ({'Доход' if self.is_income else 'Витрата'})"


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # Наприклад: 'USD', 'EUR', 'UAH'
    name = models.CharField(max_length=50)  # Наприклад: 'US Dollar'
    symbol = models.CharField(max_length=5)  # Наприклад: '$', '₴'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="currencies",
    )

    def __str__(self):
        return f"{self.symbol} ({self.code})"

class User(AbstractUser):

    class Meta:
        ordering = ("username",)


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency.code}"


