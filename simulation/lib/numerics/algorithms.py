import numpy as np


def vec_midpoint(f, a, b, n, g=None, c=None):
    h = (b - a)/n
    x = np.linspace(a+h/2, b-h/2, n)
    if callable(g):
        return np.sum(f(x, g(x, c)))
    return np.sum(f(x, g))*h


def trapezoidal(f, a, b, n, g=None, c=None):
    h = (b - a)/n
    x = np.linspace(a, b, n)
    if callable(g):
        return np.sum(f(x, g(x, c)))
    return np.sum(f(x, g))*h
