import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import BayesianRidge

data_path = 'F:\Rutgers\\2ndSemester\SOFTWR ENGG WEB APPL\Homework\Project\data\year_data\\AMZN.json'
origin_data = json.load(open(data_path))

# get stock data
#x_train = np.array(origin_data["time"][0:10]).reshape(-1, 1)
#y_train = np.array(origin_data["low"][0:100])
#x_train = np.array(range(1, len(y_train) + 3)).reshape(-1, 1)
#x_test = np.array(origin_data["time"][0:10]).reshape(-1, 1)
#y_test = np.array(origin_data["low"][0:110])
#x_test = np.array(range(1, len(y_test) + 10)).reshape(-1, 1)

#print(x_train)
#print(y_train)


class bcf():
    def __init__(self, trainX, trainY):
        self.model = None
        self.t_X = trainX
        self.t_Y = trainY.reshape(len(trainY), 1)
        self.lambd = 0.02
        self.M = 9

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


def experiment():
    pre_Y = []
    real_Y = []
    pre_T = []
    real_T = []
    for i in range(101):
        y_train = np.array(origin_data["low"][0:100 + i])
        x_train = np.array(range(100, len(y_train) + 100)).reshape(-1, 1)
        y_test = np.array(origin_data["low"][0:i + 100 + 3])
        x_test = np.array(range(1000, len(y_test) + 1000)).reshape(-1, 1)

        BCF = bcf(x_train, y_train)
        res = BCF.predict(x_test)
        pre_y = res[-1]
        real_y = y_test[-1]

        pre_Y.append(pre_y)
        real_Y.append(real_y)

        pre_trend = res[-1] - res[-2]
        real_trend = y_test[-1] - y_test[-2]
        pre_T.append(pre_trend)
        real_T.append(real_trend)
        #print('pt', res)

    tp = tn = fp = fn = 0
    #print(pre_T)
    for pre, real in zip(pre_T, real_T):
        print(pre[0], real)
        if pre[0] > 0 and real >= 0:
            tp += 1
        elif pre[0] > 0 and real < 0:
            fp += 1
        elif pre[0] < 0 and real > 0:
            fn += 1
        elif pre[0] < 0 and real <= 0:
            tn += 1
        else:
            print(pre, real)
            return 'error'

    pm = [tp, tn, fp, fn]

    fig = plt.figure(figsize=(12, 8))
    plt.scatter(x_test,
                y_test,
                facecolor="none",
                edgecolor="b",
                s=50,
                label="test point")
    plt.plot(x_test, y_test, c="g", label="test_y")
    plt.plot(x_test, res, c="r", label="pre_y")

    plt.title("Fitting Result")
    plt.legend(loc=2)
    plt.show()

    return pm, pre_Y, real_Y


pm, y_pre, y_real = experiment()
print(pm)
# result
print('True Positive Rate: ', pm[0] / (pm[0] + pm[3]))
print('True Negative Rate: ', pm[1] / (pm[1] + pm[2]))
print('Accuracy: ', (pm[0] + pm[1]) / (pm[0] + pm[1] + pm[2] + pm[3]))
print('Precision: ', pm[0] / (pm[0] + pm[2]))
print('Recall: ', pm[0] / (pm[0] + pm[3]))

axis_x = range(len(y_pre))

fig = plt.figure(figsize=(12, 8))
plt.scatter(axis_x,
            y_real,
            facecolor="none",
            edgecolor="b",
            s=50,
            label="test point")
plt.plot(axis_x, y_real, c="g", label="test_y")
plt.plot(axis_x, y_pre, c="r", label="pre_y")

plt.title("Test Result")
plt.legend(loc=2)
plt.show()

print(y_pre)
