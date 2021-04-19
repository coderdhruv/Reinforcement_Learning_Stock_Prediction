import investpy
from sklearn.cluster import KMeans
from preprocess import preprocess
import numpy as np
import datetime
import calendar
from classdefs import candlestick, actionspace, memorybufferstate, candlestickState
import random
from kmeans import Kmeans
from preprocess import preprocess


def sliding_window(df, date):
    preprocess_obj = preprocess()
    monthly_data = preprocess_obj.get_three_monthly_candlestick_data(
        df, date)
    kmeans = Kmeans(monthly_data)
    e = kmeans.get_clusters()
    print('original', e)
    l1 = []
    ctut = []
    ctlt = []
    ctbl = []
    ctc = []
    for i in range(0, len(e)):
        ctut.append(e[i][0])
        ctlt.append(e[i][1])
        ctbl.append(e[i][2])
        ctc.append(e[i][3])

    candlestickst = candlestickState(ctut, ctlt, ctbl, ctc)


def get_next_month_date(starting_date):
    starting_date_obj = datetime.datetime.strptime(
        starting_date, "%Y-%m-%d")
    total_days_first_month = calendar.monthrange(
        starting_date_obj.year, starting_date_obj.month)[1]
    next_month_starting_date = starting_date_obj + \
        datetime.timedelta(total_days_first_month)
    return next_month_starting_date.strftime("%Y-%m-%d")


def select_random_action():
    action_state = random.randint(1, 3)
    if action_state == 1:
        return 'Hold'
    if action_state == 2:
        return 'Long'
    if action_state == 3:
        return 'Short'


def get_reward(date):
    preprocess_obj = preprocess()
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    num_days = preprocess_obj.get_next_three_months_days(date)
    next_three_month_date = starting_date_obj + \
        datetime.timedelta(num_days)

    df = investpy.get_stock_historical_data(
        stock='AAPL', country='United States', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_three_month_date.strftime("%d/%m/%Y"))
    print(df)


# def fill_with_random_action_value(df, date):
#     for i in range(0, 12):
df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/2010', to_date='01/01/2020')

print(get_reward('2010-01-01'))
