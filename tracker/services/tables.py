from django.db.models import Sum, Q, Max, F
from tracker.models import Transaction, Category




class RecentTransactions:
    def __init__(self, request):
        self.user = request.user

    def get_recent_transactions(self, limit=10, month=None):
        queryset = Transaction.objects.filter(user=self.user).select_related("currency", "category")
        if month:
            queryset = queryset.filter(date__month=month)
        return queryset.order_by("-date")[:limit]


class TopExpenses:
    def __init__(self, request):
        self.user = request.user

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.user)
        return queryset

    @staticmethod
    def total_amount(queryset):
        return queryset.annotate(
            total_expense=Sum(
                "transaction__amount",
                filter=Q(transaction__type="expense")
            ),
            last_date=Max(
                "transaction__date",
                filter=Q(transaction__type="expense")
            ),
            currency_symbol=F("transaction__currency__symbol"),
        )

    def expenses(self):
        qs = self.get_queryset()
        qs = self.total_amount(qs)
        # При бажанні: відфільтрувати категорії без витрат
        qs = qs.filter(total_expense__gt=0).order_by("-total_expense")
        return qs


