from money.models import Currencies, ExchangeRates


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context


def get_main_currencie():
    return Currencies.objects.filter(code='980')[:1][0]


def get_regulated_sum(date, currencie, sum_to_convert):
    reg_currencie = get_main_currencie()
    if reg_currencie.pk == currencie.pk:
        return sum_to_convert
    else:
        rs = ExchangeRates.objects.filter(currencie=currencie, date__lte=date).values_list('value', flat=True).order_by(
            '-id')[:1]
        if rs.exists():
            return sum_to_convert * rs[0]
        else:
            return 0
