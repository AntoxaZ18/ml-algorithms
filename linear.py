
import pandas as pd
import numpy as np

from sklearn import datasets, linear_model
import matplotlib.pyplot as plt

class MyLineReg:
    def __init__(self, n_iter = 50, learning_rate = 0.1, weights = None):
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.weights = weights

    def __str__(self):
        return f'MyLineReg class: n_iter={self.n_iter}, learning_rate={self.learning_rate}'
    
    def fit(self, X: pd.DataFrame, y: pd.DataFrame, verbose=False):
        # y = y.to_numpy()
        # X = X.to_numpy()
        observations, features = X.shape
        X = np.hstack((np.ones(observations).reshape(observations, 1), X))    #add extra column

        self.weights = np.ones((features + 1, 1))

        for i in range(self.n_iter):
            y_pred = X.dot(self.weights).sum(axis=1)
            print('y_pred', y_pred.shape, X.shape, self.weights.shape)
            err = y_pred - y
            # print('error', err.shape)
            grad = 2 / observations * X.T.dot(err)

            error = self.learning_rate * grad
            self.weights = self.weights - (self.learning_rate * grad).reshape(features, 1)
            if verbose and i % int(verbose) == 0:
                print(f'{i}|loss: {err.sum()}')
        
    def get_coef(self):
        return self.weights




m = MyLineReg()


X, y = datasets.load_diabetes(return_X_y=True)

# Split the data into training/testing sets
X_train = X[:-20]
X_test = X[-20:]

# Split the targets into training/testing sets
y_train = y[:-20]
y_test = y[-20:]

m.fit(X_train, y_train, 5)
# print(m.weights.shape)
# regr = linear_model.LinearRegression()

# # Train the model using the training sets
# regr.fit(X_train, y_train)