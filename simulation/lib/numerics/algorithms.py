import numpy as np


def vec_midpoint(f, a, b, n, g=None, c=None):
    h = (b - a)/n
    x = np.linspace(a+h/2, b-h/2, n)
    if callable(g):
        return np.sum(f(x, g(x, c)))*h
    elif g is None:
        return np.sum(f(x))*h
    return np.sum(f(x, g))*h


def trapezoidal(f, a, b, n, g=None, c=None):
    h = (b - a)/n
    x = np.linspace(a, b, n)
    s = 0
    if callable(g):
        s += np.trapz(f(x, g(x, c)), x=x, dx=h)
    elif g is None:
        s += np.trapz(f(x), x=x, dx=h)
    else:
        s += np.trapz(f(x, g), x=x, dx=h)
    return s