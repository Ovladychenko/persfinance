from datetime import timedelta, date, datetime
import datetime
import requests
import json
import calendar


def get_colors(count):
    colors = [
        '#FF0000',
        '#800000',
        '#FFFF00',
        '#808000',
        '#00FF00',
        '#008000',
        '#00FFFF',
        '#008080',
        '#0000FF',
        '#000080',
        '#FF00FF'
    ]
    return colors[:count]


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def get_array_date_between(start_date, end_date):
    result = []
    for dt in date_range(start_date, end_date):
        result.append(dt)
    return result


def add_months_to_date(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def diff_month_count(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def get_array_date_between(start_date, end_date):
    periods = []
    count_month = diff_month_count(end_date, start_date) + 1
    date_value = start_date.replace(day=1)

    for i in range(0, count_month):
     date_s = add_months_to_date(date_value, i)
     periods.append(date_s)

    return periods

def get_name_month_by_number(date_value):
    month = ('январь',
             'февраль',
             'март',
             'апрель',
             'май',
             'июнь',
             'июль',
             'август',
             'сентябрь',
             'октябрь',
             'ноябрь',
             'декабрь'
             )
    return month[date_value.month-1]

def get_period_month(start_date, end_date):
    result = dict()
    periods = get_array_date_between(start_date, end_date)
    for p in periods:
        result[p] = 0
    return result
