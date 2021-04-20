import investpy
from sklearn.cluster import KMeans
from preprocess import preprocess
import numpy as np
import datetime
import calendar
from classdefs import candlestick, actionspace, memorybufferstate, candlestickState, memorybuffer
import random
from kmeans import Kmeans
from preprocess import preprocess


def sliding_window_three_months(df, date):
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    preprocess_obj = preprocess()
    monthly_data = preprocess_obj.get_three_monthly_candlestick_data(
        df, date)
    kmeans = Kmeans(monthly_data)
    e = kmeans.get_clusters()
    print('original', e)
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
    return candlestickst


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


def get_action_for_training(df, date):
    preprocess_obj = preprocess()
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    num_days_next_three_months = preprocess_obj.get_next_three_months_days(
        date)
    num_days_next_two_months = preprocess_obj.get_next_two_months_days(date)
    next_three_month_date = starting_date_obj + \
        datetime.timedelta(num_days_next_three_months)
    next_two_month_date = starting_date_obj + \
        datetime.timedelta(num_days_next_two_months)
    df_opening_calc = investpy.get_stock_historical_data(
        stock='SBI', country='India', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_two_month_date.strftime("%d/%m/%Y"))
    df_closing_calc = investpy.get_stock_historical_data(
        stock='SBI', country='India', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_three_month_date.strftime("%d/%m/%Y"))

    # to calculate date till it is found in df
    next_three_month_date_temp = next_three_month_date
    while next_three_month_date_temp not in df.index:
        next_three_month_date_temp = next_three_month_date_temp - \
            datetime.timedelta(1)

    # to calculate date till it is found in df
    next_two_month_date_temp = next_two_month_date
    while next_two_month_date_temp not in df.index:
        next_two_month_date_temp = next_two_month_date_temp - \
            datetime.timedelta(1)

    if df_closing_calc.loc[next_three_month_date_temp]['Close'] > df_opening_calc.loc[next_two_month_date_temp]['Close']:
        return 'Long'
    elif df_closing_calc.loc[next_three_month_date_temp]['Close'] < df_opening_calc.loc[next_two_month_date_temp]['Close']:
        return 'Short'
    else:
        return 'Hold'


def get_reward(df, date, actionstate):
    preprocess_obj = preprocess()
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    num_days_next_three_months = preprocess_obj.get_next_three_months_days(
        date)
    num_days_next_two_months = preprocess_obj.get_next_two_months_days(date)
    next_three_month_date = starting_date_obj + \
        datetime.timedelta(num_days_next_three_months)
    next_two_month_date = starting_date_obj + \
        datetime.timedelta(num_days_next_two_months)
    df_opening_calc = investpy.get_stock_historical_data(
        stock='SBI', country='India', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_two_month_date.strftime("%d/%m/%Y"))
    df_closing_calc = investpy.get_stock_historical_data(
        stock='SBI', country='India', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_three_month_date.strftime("%d/%m/%Y"))

    #print('opening', df_opening_calc)
    #print('closing', df_closing_calc)
    # to calculate date till it is found in df
    next_three_month_date_temp = next_three_month_date
    while next_three_month_date_temp not in df.index:
        next_three_month_date_temp = next_three_month_date_temp - \
            datetime.timedelta(1)

    # to calculate date till it is found in df
    next_two_month_date_temp = next_two_month_date
    while next_two_month_date_temp not in df.index:
        next_two_month_date_temp = next_two_month_date_temp - \
            datetime.timedelta(1)

    if actionstate == 'Long':
        return df_closing_calc.loc[next_three_month_date_temp]['Close'] - df_opening_calc.loc[next_two_month_date_temp]['Close']
    if actionstate == 'Short':
        return -(df_closing_calc.loc[next_three_month_date_temp]['Close'] - df_opening_calc.loc[next_two_month_date_temp]['Close'])
    if actionstate == 'Hold':
        return 0


def fill_state_action_reward_values(df, date):
    candlestickState = sliding_window_three_months(df, date)
    #action = select_random_action()
    action = get_action_for_training(df, date)
    reward = get_reward(df, date, action)
    memorybufferState = memorybufferstate(candlestickState, action, reward)
    memorybuffer.append(memorybufferState)


def cumulative_before_n_trading_times_calc(df, date):
    fill_state_action_reward_values(df, date)
    for i in range(0, 11):
        date = get_next_month_date(date)
        fill_state_action_reward_values(df, date)


def get_loaded_memory_buffer(df, date):
    cumulative_before_n_trading_times_calc(df, date)
    return memorybuffer


df = investpy.get_stock_historical_data(
    stock='SBI', country='India', from_date='01/01/1981', to_date='01/01/2021')

print(df)

cumulative_before_n_trading_times_calc(df, '2017-01-01')
for i in range(0, len(memorybuffer)):
    print(memorybuffer[i].candlestickstate.centreofut)
    print(memorybuffer[i].candlestickstate.centreoflt)
    print(memorybuffer[i].candlestickstate.centreofbl)
    print(memorybuffer[i].candlestickstate.centreofcolor)
    print(memorybuffer[i].action)
    print(memorybuffer[i].reward)
