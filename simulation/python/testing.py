from math import sin, cos, atan, sqrt, exp
import matplotlib.pyplot as plt
import numpy as np
import numba
from time import perf_counter

D = 20
N = 10_000
v = 1
h = (D/N)
smax = 0.9

def dx(x):
    return (f(x+h)-f(x-h))/(2*h)
    
S = lambda x: smax*np.exp(-np.power((np.power(x, 1.2)-D/1.5), 4)/200)
T1 = lambda x: 1/np.sqrt(np.power(v, 2) - np.power(S(x), 2))

def trapezoidal(f, a, b, n):
    """
    f -- A given function
    a -- Is the start
    b -- Is the end
    n -- Number of slices

    returns the array under the function, which in this case is equal to the time
    This is a implementation of the trapezoidal algorithm with a uniform grid.
    """
    x = 0 
    x += (f(a)/2)
    for i in range(1, n):
        x += f(a + i*h)
    x += (f(b)/2)
    return x*h

def vec_midpoint(f, a, b, n):
    h = (b - a)/n
    x = np.linspace(a+h/2, b-h/2, n)
    return np.sum(f(x))*h

s = np.linspace(0, D, N)
x = np.linspace(0, D, N)
start = perf_counter()
print(f"{trapezoidal(T1, 0, D, N):.5f}s")
print(f"time={perf_counter() - start}")
start = perf_counter()
print(f"{vec_midpoint(T1, 0, D, N):.5f}s")
print(f"time={perf_counter() - start}")
#y = np.sum(T1(y))
#plt.plot([0, D], [0, 0])
#plt.plot(x, y)
#plt.xlabel("X-akse, x(m)")
#plt.ylabel("Y-akse, y(m)")
#plt.show()