import investpy
from sklearn.cluster import KMeans
from preprocess import preprocess
import numpy as np
import datetime
import calendar


class Kmeans:
    def __init__(self, monthly_data):
        data_for_clustering = self.preprocess_monthly_data_to_fit_kmeans_library(
            monthly_data)
        self.kmeans = KMeans(n_clusters=5, random_state=0).fit(
            data_for_clustering)

    def preprocess_monthly_data_to_fit_kmeans_library(self, monthly_data):
        list_to_pass_kmeans_function = []
        for i in range(0, len(monthly_data)):
            temp = []
            temp.append(monthly_data[i].upper_shadow_length)
            temp.append(monthly_data[i].lower_shadow_length)
            temp.append(monthly_data[i].body_length)
            temp.append(monthly_data[i].color)
            list_to_pass_kmeans_function.append(temp)
        data_for_clustering = np.array(list_to_pass_kmeans_function)
        return data_for_clustering

    def get_clusters(self):
        return self.kmeans.cluster_centers_

    def get_labels_for_each_data_point(self):
        return self.kmeans.labels_


# df = investpy.get_stock_historical_data(
#     stock='AAPL', country='United States', from_date='01/01/2000', to_date='01/01/2001')
# print(df)
# preprocess_obj = preprocess()
# myobject = datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")
# myobject2 = datetime.datetime(2000, 1, 1, 0, 0)
# monthly_data = preprocess_obj.get_three_monthly_candlestick_data(
#     df, '2000-01-01')
# kmeans = Kmeans(monthly_data)
# print(kmeans.get_clusters())
