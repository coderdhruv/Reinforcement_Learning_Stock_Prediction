from classdefs import candlestick
import datetime
import calendar
import investpy
from sklearn.cluster import KMeans
import numpy as np


class preprocess:
    def get_monthly_candlestick_data(self, df, from_date):
        monthly_candlestick_data = []
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        total_days_current_month = calendar.monthrange(
            from_date_obj.year, from_date_obj.month)[1]
        for i in range(0, total_days_current_month):
            date_under_consideration = from_date_obj + datetime.timedelta(i)
            print(date_under_consideration, 'date')
            if date_under_consideration in df.index:
                print('good')
                Open = float(df.loc[date_under_consideration]['Open'])
                High = float(df.loc[date_under_consideration]['High'])
                Low = float(df.loc[date_under_consideration]['Low'])
                Close = float(df.loc[date_under_consideration]['Close'])
                candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                    Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
                monthly_candlestick_data.append(candlestickobj)
        return monthly_candlestick_data

    def get_three_monthly_candlestick_data(self, df, from_date):
        monthly_candlestick_data = []
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        total_days_overall = self.get_next_three_months_days(from_date)
        for i in range(0, total_days_overall):
            date_under_consideration = from_date_obj + datetime.timedelta(i)
            print(date_under_consideration, 'date')
            if date_under_consideration in df.index:
                print('good')
                Open = float(df.loc[date_under_consideration]['Open'])
                High = float(df.loc[date_under_consideration]['High'])
                Low = float(df.loc[date_under_consideration]['Low'])
                Close = float(df.loc[date_under_consideration]['Close'])
                candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                    Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
                monthly_candlestick_data.append(candlestickobj)
        return monthly_candlestick_data

    def get_upper_shadow_length(self, opens, high, low, close):
        if close >= opens:
            return high - close
        else:
            return high - opens

    def get_lower_shadow_length(self, opens, high, low, close):
        if close >= opens:
            return opens - low
        else:
            return close - low

    def get_body_length(self, opens, high, low, close):
        return abs(opens - close)

    def get_color_candlestick(self, opens, high, low, close):
        if close >= opens:
            return 1
        else:
            return 0

    def get_next_three_months_days(self, starting_date):
        starting_date_obj = datetime.datetime.strptime(
            starting_date, "%Y-%m-%d")
        total_days_first_month = calendar.monthrange(
            starting_date_obj.year, starting_date_obj.month)[1]
        second_month_starting_date = starting_date_obj + \
            datetime.timedelta(total_days_first_month)
        total_days_second_month = calendar.monthrange(
            second_month_starting_date.year, second_month_starting_date.month)[1]
        third_month_starting_date = second_month_starting_date + \
            datetime.timedelta(total_days_second_month)
        total_days_third_month = calendar.monthrange(
            third_month_starting_date.year, third_month_starting_date.month)[1]
        total_days_overall = total_days_first_month + \
            total_days_second_month + total_days_third_month
        return total_days_overall


# df = investpy.get_stock_historical_data(
#     stock='AAPL', country='United States', from_date='01/01/2000', to_date='01/01/2001')
# print(df)
# preprocess_obj = preprocess()
# myobject = datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")
# myobject2 = datetime.datetime(2000, 1, 1, 0, 0)
# monthly_data = preprocess_obj.get_three_monthly_candlestick_data(
#     df, '2000-01-01')
# print(monthly_data[0].upper_shadow_length,
#       monthly_data[0].lower_shadow_length, monthly_data[0].body_length, monthly_data[0].color)
# print(len(monthly_data))
