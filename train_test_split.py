import pandas as pd
import numpy as np
import csv

data = pd.read_csv("dataset.csv", header = None)

data = np.array(data)
n, m = data.shape

f = open("dataset_train.csv", 'a')

train_length = 300

for i in range(train_length):
    res = ""
    for j in data[i]:
        res += str(j)
        res += ','
    res = res[0: len(res)-1]
    res += '\n'
    f.write(res)

f2 = open("dataset_test.csv", 'a')

for i in range(train_length, n):
    res = ""
    for j in range(len(data[i]-2)):
        res += str(data[i][j])
        res += ','
    res += str(data[i][len(data[i])-1])
    res += '\n'
    f2.write(res)