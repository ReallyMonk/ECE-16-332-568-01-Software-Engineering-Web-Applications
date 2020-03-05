import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures


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

poly = PolynomialFeatures(9)
X_train = poly.fit_transform(x_train)
X_test = poly.fit_transform(x_test)

print(x_train)


class BayesianRegressor():
    def __init__(self, alpha=1., beta=1.):
        self.alpha = alpha
        self.beta = beta
        self.mean_prev = None
        self.S = None

    def fit(self, X, t):
        print(X.shape, t.shape)
        S_inv = self.alpha * np.eye(np.size(X, 1)) + self.beta * np.matmul(
            X.T, X)
        mean_prev = np.linalg.solve(S_inv, self.beta * np.matmul(X.T, t))
        self.mean_prev = mean_prev
        self.S = np.linalg.inv(S_inv)

    def predict(self, X):
        print(X.shape, self.mean_prev)
        y = np.matmul(X, self.mean_prev)
        y_var = 1 / self.beta + np.sum(np.matmul(X, self.S) * X, axis=1)
        y_std = np.sqrt(y_var)
        return y, y_std


'''
model = BayesianRegressor(alpha=2e-3, beta=2)
y_train = y_train.reshape(10)

print(x_train.shape)
model.fit(X_train, y_train)
y, y_std = model.predict(X_test)


fig = plt.figure(figsize=(12,8))
plt.scatter(x_train, y_train, facecolor="none", edgecolor="b", s=50, label="training data")
plt.plot(x_test, y_test, c="g", label="$\sin(2\pi x)$")
plt.plot(x_test, y, c="r", label="Mean")
#plt.fill_between(x_test, y - y_std, y + y_std, color="pink", label="std.", alpha=0.5)
plt.title("M=9")
plt.legend(loc=2)
plt.show()'''


print('---')
a = np.array([1, 2, 3]).reshape(-1, 1)
print(a)
print('---')
p = PolynomialFeatures(3)
a = p.fit_transform(a)
print(a)