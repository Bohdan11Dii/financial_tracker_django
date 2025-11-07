class CurrenciesServices:
    def __init__(self, transactions_queryset):
        self.transactions = transactions_queryset

    def get_currency_circulation(self):
        currency_totals = {}

        for transaction in self.transactions:
            currency = str(transaction.currency)  # гарантуємо рядок
            amount = transaction.amount

            if currency in currency_totals:
                currency_totals[currency] += amount
            else:
                currency_totals[currency] = amount

        result = [
            {"currency": cur, "amount": float(total)}  # float для простоти JS
            for cur, total in currency_totals.items()
        ]

        return result
