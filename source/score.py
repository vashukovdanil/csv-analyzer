from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import pandas as pd
from numpy import inf


def logReg(X_train, y_train, X_test, y_test):
    clf = LogisticRegression().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    r2_model = clf.score(X_train, y_train)
    r2_pred = r2_score(y_test, y_pred)

    return y_pred, r2_model, r2_pred

def linear(X_train, y_train, X_test, y_test):
    clf = LinearRegression().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    r2_model = clf.score(X_train, y_train)
    r2_pred = r2_score(y_test, y_pred)

    return y_pred, r2_model, r2_pred

def polynomial(X_train, y_train, X_test, y_test, polynom):
    transformer = PolynomialFeatures(degree=polynom, include_bias=False)
    X_train = transformer.fit_transform(X_train)
    X_test = transformer.fit_transform(X_test)

    X_train[X_train == -inf] = 0
    X_test[X_test == -inf] = 0

    y_pred, r2_model, r2_pred = linear(X_train, y_train, X_test, y_test)

    return y_pred, r2_model, r2_pred

def ridge(X_train, y_train, X_test, y_test, polynom):
    clf = Ridge().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    r2_model = clf.score(X_train, y_train)
    r2_pred = r2_score(y_test, y_pred)

    return y_pred, r2_model, r2_pred