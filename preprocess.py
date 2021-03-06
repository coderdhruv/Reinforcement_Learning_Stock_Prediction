from classdefs import candlestick
import datetime
import calendar
import investpy
from sklearn.cluster import KMeans
import numpy as np


class preprocess:
    def get_daily_candlestick_data(self, df, date):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        if date_obj in df.index:
            Open = float(df.loc[date_obj]['Open'])
            High = float(df.loc[date_obj]['High'])
            Low = float(df.loc[date_obj]['Low'])
            Close = float(df.loc[date_obj]['Close'])
            candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
            return candlestickobj
        else:
            return None

    def get_monthly_candlestick_data(self, df, from_date):
        monthly_candlestick_data = []
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        total_days_current_month = calendar.monthrange(
            from_date_obj.year, from_date_obj.month)[1]
        for i in range(0, total_days_current_month):
            date_under_consideration = from_date_obj + datetime.timedelta(i)
            #print(date_under_consideration, 'date')
            if date_under_consideration in df.index:
                Open = float(df.loc[date_under_consideration]['Open'])
                High = float(df.loc[date_under_consideration]['High'])
                Low = float(df.loc[date_under_consideration]['Low'])
                Close = float(df.loc[date_under_consideration]['Close'])
                print('good', Open, High, Low, Close)
                candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                    Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
                monthly_candlestick_data.append(candlestickobj)
        return monthly_candlestick_data

    def get_training_data(self, stock_name, country, from_date, to_date):
        training_data = []
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        to_date_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d")
        df = investpy.get_stock_historical_data(
            stock=stock_name, country=country, from_date=from_date_obj.strftime("%d/%m/%Y"), to_date=to_date_obj.strftime("%d/%m/%Y"))
        for i in range(0, len(df)):
            Open = float(df.iloc[i]['Open'])
            High = float(df.iloc[i]['High'])
            Low = float(df.iloc[i]['Low'])
            Close = float(df.iloc[i]['Close'])
            candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
            training_data.append(candlestickobj)
        return training_data

    def get_three_monthly_candlestick_data(self, df, from_date):
        monthly_candlestick_data = []
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        total_days_overall = self.get_next_three_months_days(from_date)
        for i in range(0, total_days_overall):
            date_under_consideration = from_date_obj + datetime.timedelta(i)
            #print(date_under_consideration, 'date')
            if date_under_consideration in df.index:
                Open = float(df.loc[date_under_consideration]['Open'])
                High = float(df.loc[date_under_consideration]['High'])
                Low = float(df.loc[date_under_consideration]['Low'])
                Close = float(df.loc[date_under_consideration]['Close'])
                candlestickobj = candlestick(self.get_upper_shadow_length(Open, High, Low, Close), self.get_lower_shadow_length(
                    Open, High, Low, Close), self.get_body_length(Open, High, Low, Close), self.get_color_candlestick(Open, High, Low, Close))
                monthly_candlestick_data.append(candlestickobj)
                # print('good', candlestickobj.upper_shadow_length,
                #       candlestickobj.lower_shadow_length, candlestickobj.body_length, candlestickobj.color)
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

    def get_next_two_months_days(self, starting_date):
        starting_date_obj = datetime.datetime.strptime(
            starting_date, "%Y-%m-%d")
        total_days_first_month = calendar.monthrange(
            starting_date_obj.year, starting_date_obj.month)[1]
        second_month_starting_date = starting_date_obj + \
            datetime.timedelta(total_days_first_month)
        total_days_second_month = calendar.monthrange(
            second_month_starting_date.year, second_month_starting_date.month)[1]
        total_days_overall = total_days_first_month + total_days_second_month
        return total_days_overall


df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/2000', to_date='01/01/2010')


# print(df)
# preprocess_obj = preprocess()
# candlestick_daily = preprocess_obj.get_daily_candlestick_data(df, '2000-01-03')
# print(candlestick_daily.upper_shadow_length,
#       candlestick_daily.lower_shadow_length)
# myobject = datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")
# myobject2 = datetime.datetime(2000, 1, 1, 0, 0)
# monthly_data = preprocess_obj.get_three_monthly_candlestick_data(
#     df, '2000-01-01')
# print(monthly_data[0].upper_shadow_length,
#       monthly_data[0].lower_shadow_length, monthly_data[0].body_length, monthly_data[0].color)
# print(len(monthly_data))
