from django.urls import path
from tracker.views import (
    index,
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,

    CurrencyListView,
    CurrencyCreateView,
    CurrencyUpdateView,
    CurrencyDeleteView,

    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,

    CreateUserView
)

urlpatterns = [
    path("", index, name="index"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),

    path("currencies/", CurrencyListView.as_view(), name="currency-list"),
    path("currencies/create/", CurrencyCreateView.as_view(), name="currency-create"),
    path("currencies/<int:pk>/update/", CurrencyUpdateView.as_view(), name="currency-update"),
    path("currencies/<int:pk>/delete/", CurrencyDeleteView.as_view(), name="currency-delete"),

    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/create/", TransactionCreateView.as_view(), name="transaction-create"),
    path("transactions/<int:pk>/update/", TransactionUpdateView.as_view(), name="transaction-update"),
    path("transactions/<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction-delete"),

    path("registration/", CreateUserView.as_view(), name="registration"),

]

app_name = "tracker"
