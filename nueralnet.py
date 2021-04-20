from preprocess import preprocess
import tensorflow as tf
from tensorflow import keras
import RL_agent
import investpy

df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/1981', to_date='01/01/2021')

membuffer = RL_agent.get_loaded_memory_buffer(df, '2010-01-01')

# (x_train, y_train), (x_val, y_val) = keras.datasets.fashion_mnist.load_data()
# print(x_train)
# print(y_train)
# print(x_val)
# print(y_val)
