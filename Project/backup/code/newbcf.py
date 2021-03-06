import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import BayesianRidge

#data_path = 'F:\Rutgers\\2ndSemester\SOFTWR ENGG WEB APPL\Homework\Project\data\year_data\\NVDA.json'
#origin_data = json.load(open(data_path))

# get stock data
#x_train = np.array(origin_data["time"][0:10]).reshape(-1, 1)
# origin_data =

#y_train = np.array(origin_data["low"][0:100])
#x_train = np.array(range(1, len(y_train) + 1)).reshape(-1, 1)

#y_test = np.array(origin_data["low"][0:101])
#x_test = np.array(range(1, len(y_test) + 1)).reshape(-1, 1)

#print(x_train)
#print(y_train)


class bcf():
    def __init__(self, trainX, trainY):
        self.model = None
        self.t_X = trainX
        self.t_Y = trainY.reshape(len(trainY), 1)
        self.lambd = 0.02
        self.M = None

    def fit(self):
        self.model = PolynomialFeatures(self.M)
        X = self.model.fit_transform(self.t_X).T
        Y = self.t_Y
        punish = self.lambd * np.identity(self.M + 1)
        w = np.matmul(np.linalg.inv(np.matmul(X, X.T) + punish),
                      np.matmul(X, Y))
        return w

    def predict(self, X):
        self.M = self.auto_adj_M()
        #print(self.M)
        w = self.fit()
        X = self.model.fit_transform(X)
        return np.matmul(w.T, X.T).T

    def auto_adj_M(self):
        err = []
        for i in range(1, 20):
            self.M = i
            w = self.fit()
            X = self.model.fit_transform(self.t_X)
            #print(w.shape)
            #print(X.shape)

            y_pre = np.matmul(w.T, X.T)
            y_real = self.t_Y.reshape(1, len(self.t_Y))
            #print(y_real)

            #print(y_pre.shape, y_pre.shape)
            err.append(
                (np.linalg.norm(y_real[0] - y_pre[0])**2) / len(y_pre[0]))
        #print(err.index(min(err)) + 1)
        return err.index(min(err)) + 1


def predict(trainX, trainY):
    trainY = np.array(trainY)
    trainX = np.array(trainX).reshape(-1, 1)
    BCF = bcf(trainX, trainY)

    res = BCF.predict(trainX + 1)

    pre_val = res[-1]
    trend = pre_val - trainY[-1]

    return pre_val, trend


'''
def experiment():
    pre_Y = []
    real_Y = []
    pre_T = []
    real_T = []
    for i in range(101):
        y_train = np.array(origin_data["low"][0:100 + i])
        x_train = np.array(range(1, len(y_train) + 1)).reshape(-1, 1)
        y_test = np.array(origin_data["low"][0:i + 100 + 1])
        x_test = np.array(range(1, len(y_test) + 1)).reshape(-1, 1)

        BCF = bcf(x_train, y_train)
        res = BCF.predict(x_test)
        pre_y = res[-1]
        real_y = y_test[-1]

        pre_Y.append(pre_y)
        real_Y.append(real_y)

        pre_trend = res[-1] - res[-2]
        #real_trend = y_test[-1] - y_test[-2]
        pre_T.append(pre_trend)
        #real_T.append(real_trend)
        #print('pt', res)

    return pre_Y, real_Y


y_pre, y_real = experiment()
print(y_pre)
print(y_real)'''