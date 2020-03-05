import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

data_path = 'D:\Rutgers\\2nd Semester\SOFTWR ENGG WEB APPL\Homework\Project\data\year_data\\NVDA.json'
origin_data = json.load(open(data_path))

#x_train = np.array(origin_data["time"][0:10]).reshape(-1, 1)
y_train = np.array(origin_data["low"][0:100])
x_train = np.array(range(1, len(y_train)+1)).reshape(-1, 1)
#x_test = np.array(origin_data["time"][0:10]).reshape(-1, 1)
y_test = np.array(origin_data["low"][0:100])
x_test = np.array(range(1, len(y_test)+1)).reshape(-1, 1)

print(x_train)
print(y_train)
'''
# for this case we create a sin(x) as the
def uniform(size):
    x = np.linspace(0, 1, size)
    return x.reshape(-1, 1)


def create_data(size):
    x = uniform(size)
    np.random.seed(42)
    y = sin_fun(x) + np.random.normal(scale=0.15, size=x.shape)
    return x, y


def sin_fun(x):
    return np.sin(2 * np.pi * x)


x_train, y_train = create_data(10)
x_test = uniform(100)
y_test = sin_fun(x_test)

'''


class Bayes_curve_fitting:
    def __init__(self, a, b, X, Y, M):
        self.a = a
        self.b = b
        self.model = PolynomialFeatures(M)
        self.t_X = self.model.fit_transform(X)
        self.t_Y = Y

    def matrixS(self):
        print(len(self.t_X[0]))
        S_inv = self.a * np.identity(len(self.t_X[0])) + self.b * np.matmul(
            self.t_X.T, self.t_X)
        return np.linalg.inv(S_inv)

    def mean(self, X):
        S = self.matrixS()
        X = self.model.fit_transform(X)
        mean = self.b * np.matmul(
            X, np.matmul(S, np.matmul(self.t_X.T, self.t_Y)))
        return mean

    def variance(self, X):
        S = self.matrixS()
        X = self.model.fit_transform(X)
        var = []
        for oneX in X:
            variance = 1 / self.b + np.matmul(oneX, np.matmul(S, oneX.T))
            var.append(np.sqrt(variance))
        return var


BCF = Bayes_curve_fitting(2e-3, 10, x_train, y_train, 9)

#y_train = y_train.reshape(100)
Mean = BCF.mean(x_test)
Std = BCF.variance(x_test)

print(Std)
print(Mean.T[0])

fig = plt.figure(figsize=(12, 8))
plt.scatter(x_train,
            y_train,
            facecolor="none",
            edgecolor="b",
            s=50,
            label="training data")
plt.plot(x_test, y_test, c="g", label="$\sin(2\pi x)$")
plt.plot(x_test, Mean, c="r", label="Mean")

plt.fill_between(x_test.T[0],
                 Mean.T - Std,
                 Mean.T + Std,
                 color="pink",
                 label="std.",
                 alpha=0.5)

plt.title("M=9")
plt.legend(loc=2)
plt.show()