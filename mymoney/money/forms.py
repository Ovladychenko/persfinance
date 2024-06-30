from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
        # fields = ['id','date', 'type', 'sum', 'sum_reg', 'counterparty', 'category', 'currencie', 'account', 'active', 'comment']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.IntegerField(required=False),
            # 'counterparty': forms.TextInput(attrs={'class': 'form-control'}),
            # 'category': forms.TextInput(attrs={'class': 'form-control'}),
            # 'currencie': forms.TextInput(attrs={'class': 'form-control'}),
            # 'account': forms.TextInput(attrs={'class': 'form-control'}),
            # 'active': forms.TextInput(attrs={'class': 'form-control'}),
            # 'comment': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'id': 'Заголовок',
            'sum': 'Сумма',
        }


class DebitDocForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), label="Дата")
    type = forms.IntegerField(required=False)
    sum = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Сумма")
    sum_reg = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    sum_reg_val = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    counterparty = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Counterparty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    account = forms.ModelChoiceField(
        label="Счет/Касса",
        queryset=MoneyAccount.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                label="Ативно", required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 8, 'rows': 4, 'class': 'form-control'}),
                              required=False, label="Комментарий")


class CreditDocForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), label="Дата")
    type = forms.IntegerField(required=False)
    sum = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Сумма")
    sum_reg = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    sum_reg_val = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    counterparty = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Counterparty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    account = forms.ModelChoiceField(
        label="Счет/Касса",
        queryset=MoneyAccount.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                label="Ативно", required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 8, 'rows': 4, 'class': 'form-control'}),
                              required=False, label="Комментарий")


class ExchangeRatesForm(forms.ModelForm):
    class Meta:
        model = ExchangeRates
        fields = "__all__"
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'currencie': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Дата',
            'currencie': 'Валюта',
            'value': 'Курс',
        }

class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'cols': 10, 'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'name': 'Наименование',
            'comment': 'Комментарий',
        }

class CurrencieForm(forms.ModelForm):
    class Meta:
        model = Currencies
        fields = "__all__"
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'cols': 10, 'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'name': 'Наименование',
            'full_name': 'Наименование полное',
            'comment': 'Комментарий',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'cols': 10, 'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'name': 'Наименование',
            'comment': 'Комментарий',
        }

class MoneyAccountForm(forms.ModelForm):
    class Meta:
        model = MoneyAccount
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'currencie': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'cols': 10, 'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'name': 'Наименование',
            'currencie': 'Валюта',
            'comment': 'Комментарий',
        }
class ReportForm(forms.Form):
    date_start = forms.DateField(widget=DateInput)
    date_end = forms.DateField(widget=DateInput)

    #def __init__(self, *args, **kwargs):
    #    list_param1 = kwargs.pop('listparam1', None)
    #    super(ReportForm, self).__init__(*args, **kwargs)
    #    if list_param1:
    #        self.fields['listparam1'] = forms.CharField(label='Валюта',
    #                                                    widget=forms.Select(choices=list_param1))