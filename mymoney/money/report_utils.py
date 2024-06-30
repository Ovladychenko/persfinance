from datetime import timedelta, date, datetime
import datetime
import requests
import json


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
