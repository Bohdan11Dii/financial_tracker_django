from django import forms

from tracker.models import Category, Currency, Transaction, User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "is_income")



class CategorySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )

class CurrencyForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: US Dollar"
            }
        )
    )
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: 'USD', 'EUR', 'UAH'"
            }
        )
    )
    symbol = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: '$', '₴'"
            }
        )
    )

    class Meta:
        model = Currency
        fields = ("name", "code", "symbol")

class CurrencySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )
class TransactionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Example: Buy groceries"}),
        help_text="Введіть назву транзакції, наприклад: 'Купівля хліба'"
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={"placeholder": "Example: 100"}),
        help_text="Сума транзакції у вибраній валюті"
    )
    type = forms.ChoiceField(
        choices=Transaction.TRANSACTION_TYPES,
        widget=forms.RadioSelect,
        help_text="Оберіть тип транзакції: дохід або витрата"
    )
    category = forms.ModelChoiceField(
        queryset=Transaction._meta.get_field('category').remote_field.model.objects.all(),
        help_text="Категорія, до якої належить ця транзакція"
    )
    currency = forms.ModelChoiceField(
        queryset=Transaction._meta.get_field('currency').remote_field.model.objects.all(),
        help_text="Виберіть валюту транзакції"
    )

    class Meta:
        model = Transaction
        fields = ("name", "amount", "type", "category", "currency")

class TransactionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )
class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")
        help_texts = {
            'username': None,
        }
