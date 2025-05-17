from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import date
from django.views.generic import ListView, CreateView

from .forms import ExchangeRatesForm, DebitDocForm, CreditDocForm, CounterpartyForm, CurrencieForm, CategoryForm, \
    MoneyAccountForm, ReportForm
from .models import *
from .report_utils import *
from .utils import *


def index(request):
    account_sum_list = Document.objects.all() \
        .values('account__name', 'currencie__name', 'currencie__code') \
        .annotate(Sum('sum_reg')) \
        .filter(active=True)

    list_sum = list(account_sum_list)
    total = 0
    total_usd = 0
    current_date = date.today()

    for item in list_sum:
        total = total + get_regulated_sum(current_date, get_currencie_by_code(item['currencie__code']),
                                          item['sum_reg__sum'])

    total_manage = get_managerial_sum(current_date, get_manage_currencie(), total)
    total = f"{round(total, 1):,}"
    total_manage = f"{round(total_manage, 1):,}"
    context = {
        'data_list': account_sum_list,
        'total': total,
        'total_manage': total_manage,
        'main_currencie': get_main_currencie(),
        'manage_currencie': get_manage_currencie()
    }

    return render(request, 'money/index.html', context)


class DocumentList(ListView):
    template_name = 'money/documents.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return Document.objects.all().order_by('-id')


def show_doc(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)

    doc_type = doc.type
    doc_name = ""
    if request.method == 'POST':
        if doc_type == 1:
            form = DebitDocForm(request.POST)
            doc_name = "Приход"

        elif doc_type == 2:
            form = CreditDocForm(request.POST)
            doc_name = "Расход"

        if form.is_valid():
            try:
                doc.date = form.cleaned_data.get('date')
                doc.sum = form.cleaned_data.get('sum')
                currencie = get_object_or_404(MoneyAccount, pk=form.cleaned_data["account"].id).currencie
                doc.currencie = currencie
                doc.counterparty = form.cleaned_data.get('counterparty')
                doc.category = form.cleaned_data.get('category')
                doc.account = form.cleaned_data.get('account')
                doc.active = form.cleaned_data.get('active')
                doc.comment = form.cleaned_data.get('comment')
                reg_sum = get_regulated_sum(doc.date, doc.currencie, doc.sum)
                if doc_type == 1:
                    doc.sum_reg_val = reg_sum
                    doc.sum_reg = form.cleaned_data.get('sum')
                else:
                    doc.sum_reg_val = reg_sum * (-1)
                    doc.sum_reg = form.cleaned_data.get('sum') * (-1)
                doc.save()

                return redirect('docs')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:

        if doc_type == 1:
            form = DebitDocForm()
            doc_name = "Приход"
        elif doc_type == 2:
            form = CreditDocForm()
            doc_name = "Расход"
        form.fields["date"].initial = doc.date
        form.fields["sum"].initial = doc.sum
        form.fields["sum_reg"].initial = doc.sum_reg
        form.fields["counterparty"].initial = doc.counterparty
        form.fields["category"].initial = doc.category
        form.fields["account"].initial = doc.account
        form.fields["active"].initial = doc.active
        form.fields["comment"].initial = doc.comment
        form.fields["sum_reg_val"].initial = doc.sum_reg_val

    context = {
        'doc_id': doc_id,
        'form': form,
        'doc_name': doc_name
    }

    return render(request, 'money/document.html', context)


def add_debit_doc(request):
    if request.method == 'POST':
        form = DebitDocForm(request.POST)
        if form.is_valid():
            try:
                currencie = get_object_or_404(MoneyAccount, pk=form.cleaned_data["account"].id).currencie

                form.cleaned_data["type"] = 1
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"]
                form.cleaned_data["sum_reg_val"] = get_regulated_sum(form.cleaned_data["date"],
                                                                     currencie,
                                                                     form.cleaned_data["sum"])
                new_doc = Document(**form.cleaned_data)
                new_doc.currencie = currencie
                new_doc.save()

                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = DebitDocForm()
        form.fields["date"].initial = timezone.now().date()

    context = {
        'form': form
    }
    return render(request, 'money/add_debit.html', context)


def add_credit_doc(request):
    if request.method == 'POST':
        form = CreditDocForm(request.POST)
        if form.is_valid():
            try:
                currencie = get_object_or_404(MoneyAccount, pk=form.cleaned_data["account"].id).currencie
                form.cleaned_data["type"] = 2
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"] * (-1)
                form.cleaned_data["sum_reg_val"] = get_regulated_sum(form.cleaned_data["date"],
                                                                     currencie,
                                                                     form.cleaned_data["sum"]) * (-1)

                new_doc = Document(**form.cleaned_data)
                new_doc.currencie = currencie
                new_doc.save()
                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = CreditDocForm()
        form.fields["date"].initial = timezone.now().date()

    context = {
        'form': form
    }
    return render(request, 'money/add_credit.html', context)


def delete_doc(request, doc_id):
    try:
        instance = Document.objects.get(id=doc_id)
        instance.delete()
        return redirect('docs')
    except:
        print('Ошибка удаления документа')
    return render(request)


def directories(request):
    return render(request, 'money/directories.html')


class CounterpartyList(ListView):
    template_name = 'money/counterpartys.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return Counterparty.objects.all()


class ExchangeRatesList(ListView):
    template_name = 'money/exchangerates.html'

    def get_queryset(self, **kwargs):
        return ExchangeRates.objects.all()


class AddExchangeRates(DataMixin, CreateView):
    form_class = ExchangeRatesForm
    template_name = 'money/add_rate.html'
    success_url = reverse_lazy('rates_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def show_rate(request, rate_id):
    rate = get_object_or_404(ExchangeRates, pk=rate_id)
    if request.method == 'POST':
        form = ExchangeRatesForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('rates_list')
    else:
        form = ExchangeRatesForm(instance=rate)

    context = {
        'rate_id': rate_id,
        'form': form,
    }
    return render(request, 'money/rate.html', context)


def delete_rate(request, rate_id):
    try:
        instance = ExchangeRates.objects.get(id=rate_id)
        instance.delete()
        return redirect('rates_list')
    except:
        print('Ошибка удаления курса валют')
    return render(request)


def show_counterparty(request, contr_id):
    rate = get_object_or_404(Counterparty, pk=contr_id)
    if request.method == 'POST':
        form = CounterpartyForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('ctr_list')
    else:
        form = CounterpartyForm(instance=rate)

    context = {
        'contr_id': contr_id,
        'form': form,
    }
    return render(request, 'money/counterparty.html', context)


def delete_counterparty(request, contr_id):
    try:
        instance = Counterparty.objects.get(id=contr_id)
        instance.delete()
        return redirect('ctr_list')
    except:
        print('Ошибка удаления курса валют')
    return render(request)


class AddCounterpartyForm(DataMixin, CreateView):
    form_class = CounterpartyForm
    template_name = 'money/add_counterparty.html'
    success_url = reverse_lazy('ctr_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class AddCurrencieForm(DataMixin, CreateView):
    form_class = CurrencieForm
    template_name = 'money/add_currencie.html'
    success_url = reverse_lazy('cur_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class CurrenciesList(ListView):
    template_name = 'money/currencies.html'

    def get_queryset(self, **kwargs):
        return Currencies.objects.all()


def delete_currencie(request, curr_id):
    try:
        instance = Currencies.objects.get(code=curr_id)
        instance.delete()
        return redirect('cur_list')
    except:
        print('Ошибка удаления валюты')
    return render(request)


def show_currencie(request, curr_id):
    rate = get_object_or_404(Currencies, code=curr_id)
    if request.method == 'POST':
        form = CurrencieForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('cur_list')
    else:
        form = CurrencieForm(instance=rate)

    context = {
        'curr_id': curr_id,
        'form': form,
    }
    return render(request, 'money/currencie.html', context)


class CategoryList(ListView):
    template_name = 'money/categorys.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return Category.objects.all()


class AddCategoryForm(DataMixin, CreateView):
    form_class = CategoryForm
    template_name = 'money/add_category.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def show_category(request, category_id):
    rate = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=rate)

    context = {
        'category_id': category_id,
        'form': form,
    }
    return render(request, 'money/category.html', context)


def delete_category(request, category_id):
    try:
        instance = Category.objects.get(pk=category_id)
        instance.delete()
        return redirect('category_list')
    except:
        print('Ошибка удаления категории')
    return render(request)


class MoneyAccountList(ListView):
    template_name = 'money/moneyaccounts.html'

    def get_queryset(self, **kwargs):
        return MoneyAccount.objects.all()


class AddMoneyAccount(DataMixin, CreateView):
    form_class = MoneyAccountForm
    template_name = 'money/add_moneyaccount.html'
    success_url = reverse_lazy('monacn_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def show_money_account(request, monacc_id):
    money_account = get_object_or_404(MoneyAccount, pk=monacc_id)
    if request.method == 'POST':
        form = MoneyAccountForm(request.POST, instance=money_account)
        if form.is_valid():
            form.save()
            return redirect('monacn_list')
    else:
        form = MoneyAccountForm(instance=money_account)

    context = {
        'monacc_id': monacc_id,
        'form': form,
    }
    return render(request, 'money/moneyaccount.html', context)


def delete_monacc(request, monacc_id):
    try:
        instance = MoneyAccount.objects.get(pk=monacc_id)
        instance.delete()
        return redirect('monacn_list')
    except:
        print('Ошибка удаления аккаунт')
    return render(request)


# REPORTS

def reports(request):
    return render(request, 'money/reports.html')


def report_dynamic_money(request):
    dates = []
    rates = []

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('date_start')
            end_date = form.cleaned_data.get('date_end')

            rs_documents = Document.objects.filter(active=True, date__range=(start_date, end_date)).order_by('date')
            for x in rs_documents:
                dates.append(x.date.strftime("%Y-%m-%d"))
                rates.append(str(x.sum_reg))

    else:
        form = ReportForm()
        form.fields['date_start'].initial = date.today().replace(day=1)
        form.fields['date_end'].initial = date.today()

    context = {
        'form': form,
        'dates': dates,
        'rates': rates
    }
    return render(request, 'money/report_dynamic_money.html', context)


def report_credit_category(request):
    category = []
    sums = []
    colors = []
    data_detail = []
    total = 0

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('date_start')
            end_date = form.cleaned_data.get('date_end')

            rs_data = Document.objects.all() \
                .values('category__name', 'category__id') \
                .annotate(Sum('sum_reg_val')) \
                .filter(active=True, type=2, date__range=(start_date, end_date)) \
                .exclude(category=5) \
                .order_by('sum_reg_val__sum')

            for x in rs_data:
                document_list = []
                total = total + (-x.get('sum_reg_val__sum'))
                category.append(x.get('category__name'))
                sums.append(str(-x.get('sum_reg_val__sum')))
                rs_document_list = Document.objects.all() \
                    .filter(active=True, type=2, date__range=(start_date, end_date), category=x.get('category__id')) \
                    .order_by('-id')
                for a in rs_document_list:
                    item_document = {
                        'id': a.id,
                        'date': a.date,
                        'account': a.account,
                        'counterparty': a.counterparty,
                        'sum_reg': a.sum_reg,
                        'currencie': a.currencie,
                        'comment': a.comment,
                    }
                    document_list.append(item_document)

                item_data = {
                    'caption': x.get('category__name') + "  " + str(-x.get('sum_reg_val__sum')),
                    'documents': document_list,
                }
                data_detail.append(item_data)

            colors = get_colors(len(category))

    else:
        form = ReportForm()
        form.fields['date_start'].initial = date.today().replace(day=1)
        form.fields['date_end'].initial = date.today()

    context = {
        'form': form,
        'managers': category,
        'percents': sums,
        'colors': colors,
        'data_detail': data_detail,
        'total': total,
    }
    return render(request, 'money/report_credit_category.html', context)


def report_debit_credit_line(request):
    labels = []
    debit_value = []
    credit_value = []

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('date_start')
            end_date = form.cleaned_data.get('date_end')

            sql_debit = '''
            SELECT 
            date(date, 'start of month') as Date,
            sum(sum_reg_val) as Sum,
            max(id) as id
            FROM 
            (  SELECT * FROM money_document)
            where
            active = true and type = %s
            and date >= %s and  date <= %s
             group by date(date, 'start of month')
             order by date(date, 'start of month')
            '''
            periods = get_period_month(start_date, end_date)
            for period_item in periods:
                labels.append(get_name_month_by_number(period_item) + ' ' + str(period_item.year))

            debit_data = Document.objects.raw(sql_debit, [1, start_date, get_end_of_month(end_date)])
            for p in debit_data:
                date_separate = p.Date.split("-")
                date_object = date(int(date_separate[0]), int(date_separate[1]), int(date_separate[2]))
                periods[date_object] = p.Sum

            debit_value = list(periods.values())

            for key in periods:
                periods[key] = 0

            credit_data = Document.objects.raw(sql_debit, [2, start_date, end_date])
            for p in credit_data:
                date_separate = p.Date.split("-")
                date_object = date(int(date_separate[0]), int(date_separate[1]), int(date_separate[2]))
                periods[date_object] = -p.Sum

            credit_value = list(periods.values())
    else:
        form = ReportForm()
        form.fields['date_start'].initial = date.today().replace(day=1)
        form.fields['date_end'].initial = date.today()

    datasets = [
        {
            'label': 'Дебет',
            'data': debit_value,
            'borderColor': 'blue',
            'backgroundColor': 'blue',
        },
        {
            'label': 'Кредит',
            'data': credit_value,
            'borderColor': 'red',
            'backgroundColor': 'red',
        }
    ]

    context = {
        'form': form,
        'data':
            {
                'labels': labels,
                'datasets': datasets
            }
    }
    return render(request, 'money/report_debit_credit_line.html', context)


def report_debit_credit_bar(request):
    labels = []
    debit_value = []
    credit_value = []
    counterparties = []
    categories = []
    datasets = []
    debit_total_value = []
    credit_total_value = []

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('date_start')
            end_date = form.cleaned_data.get('date_end')

            periods = get_period_month(start_date, end_date)
            debit_total_value = dict.fromkeys(periods.copy(), 0)
            credit_total_value = dict.fromkeys(periods.copy(), 0)
            for period_item in periods:
                labels.append(get_name_month_by_number(period_item) + ' ' + str(period_item.year))

            sql_debit = '''
            SELECT 
             date(date, 'start of month') as Date,
             name,
             sum(sum_reg_val) as Sum,
             max(id) as id
           FROM 
             ( 
               SELECT
                    *,
                    money_counterparty.name as name 
                FROM money_document
                LEFT JOIN money_counterparty
                ON money_document.counterparty_id = money_counterparty.id)
            where
            active = true and type = 1 and counterparty_id <> 5
            and date >= %s and  date <= %s
             group by date(date, 'start of month'),counterparty_id
             order by date(date, 'start of month')
            '''

            debit_rs = Document.objects.raw(sql_debit, [start_date, end_date])
            for p in debit_rs:
                date_separate = p.Date.split("-")
                date_object = date(int(date_separate[0]), int(date_separate[1]), int(date_separate[2]))

                debit_item = {'period': date_object, 'name': p.name, 'sum': p.Sum}
                debit_value.append(debit_item)
                counterparties.append(p.name)
                # for debit total
                debit_total_value[date_object] += p.Sum

            counterparties_list = list(set(counterparties))

            colors_debit = get_colors_debit(len(counterparties_list))
            step = 0
            for counterparty_item in counterparties_list:
                periods_counterparty = dict.fromkeys(periods.copy(), 0)
                counterparty_data_list = [x for x in debit_value if x['name'] == counterparty_item]

                for record_item in counterparty_data_list:
                    period = record_item['period']
                    periods_counterparty[period] = record_item['sum']

                dataset_item = {'label': counterparty_item, 'data': list(periods_counterparty.values()),
                                'backgroundColor': colors_debit[step], 'stack': 'Дебит1'}
                datasets.append(dataset_item)
                step += 1

            sql_credit = '''
                 SELECT 
                 date(date, 'start of month') as Date,
                 sum(sum_reg_val) as Sum,
                 max(id) as id,
                 name
                 FROM 
                 (  SELECT *,
                 money_category.name as name 
                  FROM money_document
                 
                LEFT JOIN money_category
                ON money_document.category_id = money_category.id)
                 where
                 active = true and type = %s
                 and date >= %s and  date <= %s
                  group by date(date, 'start of month'),name
                  order by date(date, 'start of month')
                 '''

            credit_rs = Document.objects.raw(sql_credit, [2, start_date, end_date])
            for p in credit_rs:
                date_separate = p.Date.split("-")
                date_object = date(int(date_separate[0]), int(date_separate[1]), int(date_separate[2]))

                credit_item = {'period': date_object, 'name': p.name, 'sum': -p.Sum}
                credit_value.append(credit_item)
                categories.append(p.name)

                # for debit total
                credit_total_value[date_object] += -p.Sum

            categories_list = list(set(categories))
            colors_credit = get_colors_credit(len(categories_list))
            step = 0
            for category_item in categories_list:
                periods_categories = dict.fromkeys(periods.copy(), 0)
                counterparty_data_list = [x for x in credit_value if x['name'] == category_item]

                for record_item in counterparty_data_list:
                    period = record_item['period']
                    periods_categories[period] = record_item['sum']

                dataset_item = {'label': category_item, 'data': list(periods_categories.values()),
                                'backgroundColor': colors_credit[step], 'stack': 'Кредит'}
                datasets.append(dataset_item)
                step += 1

            credit_total_value = list(credit_total_value.values())
            debit_total_value = list(debit_total_value.values())
    else:
        form = ReportForm()
        form.fields['date_start'].initial = date.today().replace(day=1)
        form.fields['date_end'].initial = date.today()

    dataset_total = [
        {
            'label': 'Дебет',
            'data': debit_total_value,
            'borderColor': 'blue',
            'backgroundColor': 'blue',
            'stack': 'Дебит1',
        },
        {
            'label': 'Кредит',
            'data': credit_total_value,
            'borderColor': 'red',
            'backgroundColor': 'red',
            'stack': 'Кредит',
        }
    ]

    context = {
        'form': form,
        'data':
            {
                'labels': labels,
                'datasets': datasets
            },
        'data_total':
            {
                'labels': labels,
                'datasets': dataset_total
            },

    }
    return render(request, 'money/report_debit_credit_bar.html', context)
