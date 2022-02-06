import numpy as np


def vec_midpoint(f, a, b, n, g=0, theta=0):
    h = (b - a)/n
    x = np.linspace(a+h/2, b-h/2, n)
    return np.sum(f(x, g(x, theta)))*h


def trapezoidal(f, start, end, n, g, theta):
    h = float(end - start) / n
    section = 0.0
    section += f(start, g(start, theta))/2.0
    for i in range(1, n):
        section += f(start + i*h, g(start + i*h, theta))
    section += f(end, g(end, theta))/2.0
    return section * h

def fdx(f, x, h, y):
    return (f(x+h, y)-f(x-h, y))/(2*h)

def fdy(f, x, h, y):
    return (f(x, y+h)-f(x, y-h))/(2*h)