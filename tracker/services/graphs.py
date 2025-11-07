from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict


class IncomeExpenseSchedule:
    def __init__(self, transactions_queryset):
        self.transactions = transactions_queryset

    def get_income_expense_data(self):
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)

        transactions = self.transactions.filter(
            date__gte=month_ago
        ).values('date', 'type').annotate(total=Sum('amount'))

        data = defaultdict(lambda: {'income': 0, 'expense': 0})

        for t in transactions:
            date = t['date'].strftime('%b %d')  # 'Aug 01'
            data[date][t['type']] = float(t['total'])

        labels = list(sorted(data.keys()))
        income = [data[day]['income'] for day in labels]
        expense = [data[day]['expense'] for day in labels]

        return {
            'labels': labels,
            'income': income,
            'expense': expense,
        }

