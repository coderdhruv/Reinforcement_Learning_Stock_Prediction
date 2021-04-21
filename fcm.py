import investpy
from sklearn.cluster import KMeans
from preprocess import preprocess
import numpy as np
import datetime
import calendar
from fcmeans import FCM


class FCmeans:
    def __init__(self, monthly_data):
        data_for_clustering = self.preprocess_monthly_data_to_fit_fcmeans_library(
            monthly_data)
        self.fcmeans = FCM(n_clusters=5, random_state=0)
        self.fcmeans.fit(data_for_clustering)

    def preprocess_monthly_data_to_fit_fcmeans_library(self, monthly_data):
        list_to_pass_fcmeans_function = []
        for i in range(0, len(monthly_data)):
            temp = []
            temp.append(monthly_data[i].upper_shadow_length)
            temp.append(monthly_data[i].lower_shadow_length)
            temp.append(monthly_data[i].body_length)
            temp.append(monthly_data[i].color)
            list_to_pass_fcmeans_function.append(temp)
        data_for_clustering = np.array(list_to_pass_fcmeans_function)
        return data_for_clustering

    def get_clusters(self):
        return self.fcmeans.centers

    # def get_labels_for_each_data_point(self):
    #     return self.fcmeans.predict(monthly_data)


class FCmeansDaily:
    def __init__(self, training_data):
        data_for_clustering = self.preprocess_monthly_data_to_fit_fcmeans_library(
            training_data)
        self.fcmeans = FCM(n_clusters=5, random_state=0)
        self.fcmeans.fit(data_for_clustering)

    def preprocess_daily_data_to_fit_fcmeans_library(self, training_data):
        list_to_pass_kmeans_function = []
        for i in range(0, len(training_data)):
            temp = []
            temp.append(training_data[i].upper_shadow_length)
            temp.append(training_data[i].lower_shadow_length)
            temp.append(training_data[i].body_length)
            temp.append(training_data[i].color)
            list_to_pass_kmeans_function.append(temp)
        data_for_clustering = np.array(list_to_pass_kmeans_function)
        return data_for_clustering

    def get_clusters(self):
        return self.fcmeans.centers

    def get_labels_list(self):
        X = self.preprocess_monthly_data_to_fit_fcmeans_library(
            training_data)
        return self.fcm.predict(X)

    def get_labels_for_each_data_point(self, data_point_index):
        return self.get_labels_list()[data_point_index]


df = investpy.get_stock_historical_data(
    stock='AAPL', country='United States', from_date='01/01/2000', to_date='01/01/2001')
print(df)
daily_data = preprocess_obj.get_training_data(
    'AAPL', 'United States', '2000-01-01', '2000-02-01')
fcmeans = FCmeansDaily(daily_data)
print(fcmeans.get_clusters())
