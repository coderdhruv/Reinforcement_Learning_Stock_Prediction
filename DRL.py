import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv
import matplotlib.pyplot as plt
import random
data = pd.read_csv("dataset_train.csv", header = None)
data_test = pd.read_csv("dataset_test.csv", header = None)

X_train = data[data.columns[0:12]]
Y_train = data[data.columns[12:13]]

X_test = data_test[data_test.columns[0:12]]
test_reward = data_test[data_test.columns[12:13]]

Layers = [12, 12, 12, 3]

datax = np.array(X_train).T
datay = np.array(Y_train)

data_test_x = np.array(X_test)
reward = np.array(test_reward)

n, m = datax.shape
n_test, m_test = data_test.shape
# print(datax)
# print(datay)

parameterW = []
parameterB = []



def sigmoid(x):
    return 1/(1 + np.exp(-x))

def deriv_sigmoid(x):
    return x *(1 - x)

def relu(x):
    return np.maximum(0, x)

def deriv_relu(x):
    return (x > 0)

def costFunction(y, rt):
    return np.sum(np.log(np.abs(y*rt)+1))

def oneHot(Y):
    # print(Y)
    oneHot_Y = np.zeros((int(Y.size), int(Y.max()) + 1))
    for i in range(Y.size):
        oneHot_Y[i][int(Y[i][0])] = 1;
    oneHot_Y = oneHot_Y.T
    return oneHot_Y

def init_params():
    W = []
    b = []
    w1 = np.random.randn(Layers[0], n)
    b1 = np.random.randn(Layers[0], 1)
    W.append(w1)
    b.append(b1)
    for i in range(1, len(Layers)):
        w1 = np.random.randn(Layers[i], Layers[i-1])
        b1 = np.random.randn(Layers[i], 1)
        W.append(w1)
        b.append(b1)
    return W, b

def forward_prop(W, b, X):
    Z = []
    A = []
    for i in range(len(Layers)-1):
        if(i == 0):
            z1 = W[i].dot(X) + b[i]
            a1 = relu(z1)
            Z.append(z1)
            A.append(a1)
        else:
            z1 = W[i].dot(A[i-1]) + b[i]
            a1 = relu(z1)
            Z.append(z1)
            A.append(a1)
    last = len(Layers) - 1
    z1 = W[last].dot(A[last-1]) + b[last]
    a1 = sigmoid(z1)
    Z.append(z1)
    A.append(a1)
    return Z, A

def back_prop(Z, A, W, X, Y):
    m = Y.size
    one_hot_Y = oneHot(Y)
    last = len(A) - 1
    # print(one_hot_Y)
    # print(A[last])
    dz = A[last] - one_hot_Y
    dw = 1/m * dz.dot(A[last-1].T)
    db = 1/m * np.sum(dz)
    DW = [dw]
    DB = [db]
    for i in range(last-1, 0, -1):
        # print(W[i+1].shape, dz.shape, Z[i].shape)
        dz = (W[i+1].T.dot(dz)) * deriv_relu(Z[i])
        dw = 1/m * dz.dot(A[i-1].T)
        db = 1/m * np.sum(dz)
        DW.append(dw)
        DB.append(db)
    dz = W[1].T.dot(dz) * deriv_relu(Z[0])
    dw = 1/m * dz.dot(X.T)
    db = 1/m * np.sum(dz)
    DW.append(dw)
    DB.append(db)
    DW.reverse()
    DB.reverse()
    return DW, DB

def update_params(W, B, DW, DB, alpha):
    for i in range(len(W)):
        W[i] = W[i] - alpha*DW[i]
        B[i] = B[i] - alpha*DB[i]
    return W, B



def gradient_descent(X, Y, alpha, iterations):
    W, B = init_params()
    # for i in W:
    #     print(i.shape)
    Predicted = []
    parameterW = []
    parameterB = []
    for _ in range(iterations):
        Z, A = forward_prop(W, B, X)
        # for i in Z:
        #     print(i.shape)
        DW, DB = back_prop(Z, A, W, X, Y)
        # for i in DW:
        #     print(i.shape)
        W, B = update_params(W, B, DW, DB, alpha)
        if(_ == iterations-1):
            parameterW = W
            parameterB = B
            # Predicted = A[-1]

    # Predicted = Predicted.T
    # Decision = np.argmax(Predicted, 1)
    # print(Decision)
    # ODecision = []
    # for i in datay:
    #     ODecision.append(i[0])
    # print(ODecision)
    # print("Accuracy : ", accuracy_score(ODecision, Decision))
    return parameterW, parameterB
datayInt = np.zeros(datay.shape)
# print(datayInt.shape)
for i in range(datay.size):
    datayInt[i][0] = (int(datay[i][0]))

parameterW, parameterB =  gradient_descent(datax, datayInt, 0.01, 1000)

def parameter_update_using_adam(y, rt, alpha):
    t = 0
    m = 0
    u = 0
    delta = 0.001
    ep = 0.1
    beta1 = 0.3
    beta2 = 0.6
    while(t <= 100):
        t = t + 1
        g = delta*costFunction(y, rt)
        m = beta1*m + (1-beta1)*g
        u = beta2*u + (1-beta2)*g*g
        mcap = m/(1-beta1**t)
        ucap = u/(1-beta2**t)
        diff = (alpha*mcap)/(ucap**0.5 + ep)
        if(diff < 0.005):
            for i in parameterW:
                i += diff    
            for i in parameterB:
                i += diff
            break
        else:
            for i in parameterW:
                i += diff    
            for i in parameterB:
                i += diff

def predict(x):
    curData = np.zeros((12, 1))
    for i in range(len(data_test_x[x])):
        curData[i][0] = data_test_x[x][i]
    # print(curData.shape)
    tempA = []
    # for i in parameterW:
    #     print(i.shape)
    for i in range(len(parameterW)-1):
        if(i == 0):
            z1 = parameterW[i].dot(curData) + parameterB[i]
            a1 = relu(z1)
            # print("z1 : ", z1.shape)
            tempA.append(a1)
        else:
            z1 = parameterW[i].dot(tempA[i-1]) + parameterB[i]
            a1 = relu(z1)
            # print("z1 : ", z1.shape)
            tempA.append(a1)
    # print(tempA)
    last = len(Layers) - 1
    z1 = parameterW[last].dot(tempA[last-1]) + parameterB[last]
    a1 = sigmoid(z1)
    # Z.append(z1)
    tempA.append(a1)
    # print(tempA[-1].shape)
    y = np.max(tempA[-1])
    rt = reward[x][0]
    idx = np.argmax(tempA[-1])
    return idx, y, rt

finalY = np.zeros((n_test, 1))
finalRt = np.zeros((n_test, 1))
countDecision = {}
# print(reward)

plotValue = [0]
plotY = [i for i in range(n_test)]
for i in range(n_test):
    idx, y, rt = predict(i)
    randomRes = random.randint(1, 11)
    if(randomRes <= 3):
        idx = random.randint(0, 3)
        y = 1
        rt = 0
    finalY[i][0] = y
    finalRt[i][0] = rt 
    if(i%10 == 0):
        parameter_update_using_adam(finalY, finalRt, 0.01)
    decision = "";
    if(idx == 0):
        decision = "Short"
        plotValue.append(plotValue[-1]-1)
    elif (idx == 1):
        decision = "Hold"
        plotValue.append(plotValue[-1])
    else:
        decision = "Long"
        plotValue.append(plotValue[-1]+1)
    try:
        countDecision[decision] += 1
    except:
        countDecision[decision] = 1
    print("Model expects to", decision)

# print(countDecision)

# plt.bar(*zip(*countDecision.items()))
# plt.title("Count of different decision taken")
# plt.show()

# plt.plot(plotValue)
# plt.xlabel("Expected Reward in Days")
# plt.ylabel("Money gain expected")
# plt.title("Expected money flow")
# plt.show()