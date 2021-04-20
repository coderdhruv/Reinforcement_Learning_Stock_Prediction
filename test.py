from preprocess import preprocess
import investpy
import numpy as np

e = {}
df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/1981', to_date='01/01/2021')
preprocess_obj = preprocess()
candlestick_daily = preprocess_obj.get_daily_candlestick_data(df, '2000-01-03')
e[candlestick_daily] = 1

a = [2, 3, 1, 6]
b = [6, 8, 1, 3]
c = np.array(a) + np.array(b)
print(c)
