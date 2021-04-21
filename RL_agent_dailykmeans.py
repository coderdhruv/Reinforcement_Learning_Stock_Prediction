import investpy
from sklearn.cluster import KMeans
from preprocess import preprocess
import numpy as np
import datetime
import calendar
from classdefs import candlestick, actionspace, memorybufferstate, candlestickState, memorybuffer
import random
from kmeans import Kmeans, KmeansDaily
from preprocess import preprocess


def get_index_for_object(candlestickst, training_data):
    flag = -1
    for i in range(0, len(training_data)):
        if candlestickst.upper_shadow_length == training_data[i].upper_shadow_length and candlestickst.lower_shadow_length == training_data[i].lower_shadow_length and candlestickst.body_length == training_data[i].body_length and candlestickst.color == training_data[i].color:
            return i
        # if candlestickst is training_data[i]:
        #     return i
    return flag


def sliding_window_three_days(df, date, training_data):
    sliding_window_state = []
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    kmeansDaily = KmeansDaily(training_data)
    preprocess12 = preprocess()
    candlestickstate = preprocess12.get_daily_candlestick_data(
        df, starting_date_obj.strftime("%Y-%m-%d"))
    index_of_starting_data = get_index_for_object(
        candlestickstate, training_data)
    clustercentres = kmeansDaily.get_clusters()
    print(index_of_starting_data)
    if index_of_starting_data < len(training_data):
        index_of_first_cluster_center = kmeansDaily.get_labels_for_each_data_point(
            index_of_starting_data)
        index_of_second_cluster_center = kmeansDaily.get_labels_for_each_data_point(
            index_of_starting_data + 1)
        index_of_third_cluster_center = kmeansDaily.get_labels_for_each_data_point(
            index_of_starting_data + 2)
        sliding_window_state.append(
            clustercentres[index_of_first_cluster_center])
        sliding_window_state.append(
            clustercentres[index_of_second_cluster_center])
        sliding_window_state.append(
            clustercentres[index_of_third_cluster_center])
        return sliding_window_state
    else:
        return sliding_window_state


def select_random_action():
    action_state = random.randint(1, 3)
    if action_state == 1:
        return 'Hold'
    if action_state == 2:
        return 'Long'
    if action_state == 3:
        return 'Short'


def get_action_for_training(df, date):
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    next_date_obj = starting_date_obj + datetime.timedelta(1)
    while next_date_obj not in df.index:
        next_date_obj = next_date_obj + datetime.timedelta(1)
    df = investpy.get_stock_historical_data(
        'AAPL', 'United States', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_date_obj.strftime("%d/%m/%Y"))
    next_date_close = df.loc[next_date_obj]['Close']
    start_date_close = df.loc[starting_date_obj]['Close']
    diff = next_date_close - start_date_close
    if next_date_close > start_date_close and abs(diff) > 0.03:
        return 'Long'
    elif next_date_close < start_date_close and abs(diff) > 0.03:
        return 'Short'
    else:
        return 'Hold'


def get_reward(df, date, actionstate):
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    next_date_obj = starting_date_obj + datetime.timedelta(1)
    while next_date_obj not in df.index:
        next_date_obj = next_date_obj + datetime.timedelta(1)
    df = investpy.get_stock_historical_data(
        'AAPL', 'United States', from_date=starting_date_obj.strftime("%d/%m/%Y"), to_date=next_date_obj.strftime("%d/%m/%Y"))
    next_date_close = df.loc[next_date_obj]['Close']
    start_date_close = df.loc[starting_date_obj]['Close']
    diff = next_date_close - start_date_close
    if actionstate == 'Long':
        return diff
    elif actionstate == 'Short':
        return -diff
    else:
        return 0


def fill_state_action_reward_values(df, date, training_data):
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    next_date_obj = starting_date_obj
    while next_date_obj not in df.index:
        next_date_obj = next_date_obj + datetime.timedelta(1)
    preprocess1 = preprocess()
    candlestickstate = sliding_window_three_days(
        df, next_date_obj.strftime("%Y-%m-%d"), training_data)
    #action = select_random_action()
    action = get_action_for_training(df, next_date_obj.strftime("%Y-%m-%d"))
    reward = get_reward(df, next_date_obj.strftime("%Y-%m-%d"), action)
    memorybufferState = memorybufferstate(candlestickstate, action, reward)
    memorybuffer.append(memorybufferState)


def cumulative_before_n_trading_times_calc(df, date, training_data):
    fill_state_action_reward_values(df, date, training_data)
    starting_date_obj = datetime.datetime.strptime(
        date, "%Y-%m-%d")
    next_date = starting_date_obj + datetime.timedelta(1)
    last_date = starting_date_obj + datetime.timedelta(len(training_data)-10)
    for i in range(0, len(training_data)-20):
        while next_date not in df.index and next_date < last_date:
            next_date = next_date + datetime.timedelta(1)
        if next_date < last_date:
            fill_state_action_reward_values(
                df, next_date.strftime("%Y-%m-%d"), training_data)
        next_date = next_date + datetime.timedelta(1)


def get_loaded_memory_buffer(df, date, training_data):
    cumulative_before_n_trading_times_calc(df, date, training_data)
    return memorybuffer


df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/1981', to_date='01/01/2021')

preprocess2 = preprocess()
training_data = preprocess2.get_training_data(
    'AAPL', 'United States', '2000-01-01', '2001-04-01')

print(len(training_data))
starting_date_obj1 = datetime.datetime.strptime(
    '2000-01-01', "%Y-%m-%d")
while starting_date_obj1 not in df.index:
    starting_date_obj1 = starting_date_obj1 + datetime.timedelta(1)


memorybuffer = get_loaded_memory_buffer(
    df, starting_date_obj1.strftime("%Y-%m-%d"), training_data)
# cumulative_before_n_trading_times_calc(df, '2017-01-01')
for i in range(0, len(memorybuffer)):
    for j in range(0, 3):
        if memorybuffer[i]:
            print(memorybuffer[i].candlestickstate[j])
    print(memorybuffer[i].action)
    print(memorybuffer[i].reward)
