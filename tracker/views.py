from typing import Any, Dict

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tracker.models import Category, Transaction, Currency
from tracker.forms import CategoryForm, CurrencyForm, TransactionForm, UserRegistration, CategorySearchForm, \
    TransactionSearchForm, CurrencySearchForm

from django.contrib.auth.mixins import LoginRequiredMixin

from calendar import month_name
from tracker.services.tables import RecentTransactions, TopExpenses
from tracker.services.charts import CurrenciesServices
from tracker.services.graphs import IncomeExpenseSchedule

"""Створення головної сторінки де відображатимуться всі необхідні конфігурації пов'язані з фінансовим трекером"""


@login_required
def index(request):
    transactions = Transaction.objects.filter(user=request.user).select_related("currency", "category")

    income_total = sum(t.amount for t in transactions if t.type == "income")
    expense_total = sum(t.amount for t in transactions if t.type == "expense")
    balance = income_total - expense_total

    months = [(i, month_name[i]) for i in range(1, 13)]
    selected_month = request.GET.get("month")
    recent = RecentTransactions(request).get_recent_transactions(month=selected_month)

    top_expenses = TopExpenses(request).expenses()

    order = request.GET.get("order", "desc")
    if order == "asc":
        top_expenses = top_expenses.order_by("total_expense")
    else:
        top_expenses = top_expenses.order_by("-total_expense")

    service = CurrenciesServices(transactions)
    currency_sums = service.get_currency_circulation()

    chart_data = IncomeExpenseSchedule(transactions).get_income_expense_data()

    print(chart_data)

    context = {
        "balance": balance,
        "income_total": income_total,
        "expense_total": expense_total,

        "recent": recent,
        "months": months,
        "selected_month": int(selected_month) if selected_month else "",

        "top_expenses": top_expenses,

        "currency_sums": currency_sums,

        "chart_labels": chart_data["labels"],
        "chart_income": chart_data["income"],
        "chart_expense": chart_data["expense"],

    }

    return render(request, "tracker/main/main.html", context)


"""Створення категорій і повноцінний CRUD"""


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = "tracker/category/category_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(
            initial={
                "name": name
            }
        )
        return context

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        form = CategorySearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "tracker/category/category_form.html"
    success_url = reverse_lazy("tracker:category-list")

    def form_valid(self, form):
        # Передаємо користувача у метод save форми
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "tracker/category/category_form.html"
    success_url = reverse_lazy("tracker:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("tracker:category-list")
    template_name = "tracker/category/category_confirm_delete.html"


"""Створення валюти і повноцінний CRUD"""


class CurrencyListView(LoginRequiredMixin, generic.ListView):
    model = Currency
    template_name = "tracker/currency/currency_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CurrencyListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CurrencySearchForm(
            initial={
                "name": name
            }
        )
        return context

    def get_queryset(self):
        queryset = Currency.objects.filter(user=self.request.user)
        form = CurrencySearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class CurrencyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "tracker/currency/currency_form.html"
    success_url = reverse_lazy("tracker:currency-list")

    def form_valid(self, form):
        # Передаємо користувача у метод save форми
        form.instance.user = self.request.user
        return super().form_valid(form)


class CurrencyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "tracker/currency/currency_form.html"
    success_url = reverse_lazy("tracker:currency-list")


class CurrencyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Currency
    success_url = reverse_lazy("tracker:currency-list")
    template_name = "tracker/currency/currency_confirm_delete.html"


"""Створення транзакцій і повноцінний CRUD"""


class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = "tracker/transaction/transaction_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(TransactionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TransactionSearchForm(
            initial={
                "name": name
            }
        )
        return context

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related('currency', 'category')
        form = TransactionSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class TransactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    context_object_name = "transaction"
    form_class = TransactionForm
    template_name = "tracker/transaction/transaction_form.html"
    success_url = reverse_lazy("tracker:transaction-list")

    def form_valid(self, form):
        # Передаємо користувача у метод save форми
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transaction/transaction_form.html"
    success_url = reverse_lazy("tracker:transaction-list")


class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    template_name = "tracker/transaction/transaction_confirm_delete.html"
    success_url = reverse_lazy("tracker:transaction-list")


"""Реєстрація нового користувача"""


class CreateUserView(generic.CreateView):
    form_class = UserRegistration
    template_name = "registration/register.html"
    success_url = reverse_lazy("tracker:index")

    def form_valid(self, form):
        user = form.save()

        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()

        login(self.request, user)

        return super().form_valid(form)
