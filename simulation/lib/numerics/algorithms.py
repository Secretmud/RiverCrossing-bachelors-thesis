import numpy as np


def vec_midpoint(f, a, b, n, g=None, c=None):
    h = (b - a)/n
    x = np.linspace(a+h/2, b-h/2, n)
    if callable(g):
        return np.sum(f(x, g(x, c)))*h
    return np.sum(f(x, g))*h


def trapezoidal(f, a, b, n, g=None, c=None):
    """
    h = (b-a)/float(n)
    x = np.linspace(a, b, n)
    if callable(g):
        s = 0.5*(f(a, g(x, c)) + f(b, g(x, c)))
        for i in range(1,n,1):
            s = s + f(a + i*h, g(x, c))
    else:
        s = 0.5*(f(a, g) + f(b, g))
        for i in range(1,n,1):
            s = s + f(a + i*h, g)
    return h*s
    """
    h = (b - a)/n
    x = np.linspace(a, b, n)
    if callable(g):
        return np.sum(f(x, g(x, c)))*h
    return np.sum(f(x, g))*h