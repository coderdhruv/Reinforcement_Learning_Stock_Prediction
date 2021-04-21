from preprocess import preprocess
import tensorflow as tf
from tensorflow import keras
import RL_agent_dailykmeans
import investpy
import datetime

df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/1981', to_date='01/01/2021')

preprocess2 = preprocess()
training_data = preprocess2.get_training_data(
    'AAPL', 'United States', '2000-01-01', '2000-02-01')

starting_date_obj1 = datetime.datetime.strptime(
    '2000-01-01', "%Y-%m-%d")
while starting_date_obj1 not in df.index:
    starting_date_obj1 = starting_date_obj1 + datetime.timedelta(1)
memorybuffer = RL_agent_dailykmeans.get_loaded_memory_buffer(
    df, starting_date_obj1.strftime("%Y-%m-%d"), training_data)
print(memorybuffer)
# (x_train, y_train), (x_val, y_val) = keras.datasets.fashion_mnist.load_data()
# print(x_train)
# print(y_train)
# print(x_val)
# print(y_val)
