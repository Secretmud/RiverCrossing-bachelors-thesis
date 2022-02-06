import numpy as np
from time import perf_counter
from lib.numerics.algorithms import vec_midpoint, trapezoidal
from lib.utils.plotting import plot_single

D = 20
N = 100
v = 1
h = (D/N)
smax = 0.9

def dx(g, x):
    return (g(x+h, 0)-g(x-h, 0))/(2*h)
    
S = lambda x: smax*np.exp(-np.power((np.power(x, 1.2)-D/1.5), 4)/200)

functions = [
    lambda x, theta: np.tan(theta) + S(x)/(v*np.cos(theta)),
    lambda x, theta: np.cos(theta) + S(x)/(v*np.tan(theta))
]
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

i = 1
time_limit = 100
theta = np.linspace(-np.pi/2, np.pi/2, N)
# This formula turns the theta array to the normal values between 0 and 2pi.
theta = (2*np.pi + theta) * (theta < 0) + theta*(theta > 0) 

for g in functions:
    mid = {}
    print(f"Function nr: {i}/{len(functions)}")
    for t in theta:
        m = vec_midpoint(T1, 0, D, N, g, t)
        if m <= time_limit:
            mid[t] = m
    lists = sorted(mid.items())
    if len(lists) > 0:
        x, y = zip(*lists)
        k = mid.keys()
        x1, y1 = min(mid.items(), key = lambda x: x[1])
        print(f"\tdegrees:\t{(x1*(180/np.pi))}/{x1}\n\ttime:\t {y1}s")
        plot_single(x, y, x1, y1)
    else:
        print(f"\tFunction {i} on midpoint found no solution where the crossing time was less or equal to {time_limit}")
    i += 1