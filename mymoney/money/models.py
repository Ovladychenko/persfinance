from django.db import models


# Create your models here.

class Document(models.Model):
    type = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    sum_reg = models.DecimalField(max_digits=10, decimal_places=2)
    counterparty = models.ForeignKey('Counterparty', on_delete=models.PROTECT, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True)
    currencie = models.ForeignKey('Currencies', on_delete=models.PROTECT, blank=True)
    active = models.BooleanField(default=True)
    comment = models.CharField(max_length=255, blank=True)
    account = models.ForeignKey('MoneyAccount', on_delete=models.PROTECT, blank=True)
    sum_reg_val = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['-date'])
        ]


class Counterparty(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Currencies(models.Model):
    code = models.CharField(max_length=3, db_index=True, primary_key=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TypeDebit(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class TypeCredit(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class MoneyAccount(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField(default=1, blank=True, null=True)  # 0- cash 1- Bank account
    currencie = models.ForeignKey('Currencies', on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class ExchangeRates(models.Model):
    currencie = models.ForeignKey('Currencies', on_delete=models.PROTECT)
    date = models.DateField()
    value = models.DecimalField('value', null=False, max_digits=10, decimal_places=5,default=0)
    multiplicity = models.IntegerField(blank=True, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['-date'])
        ]