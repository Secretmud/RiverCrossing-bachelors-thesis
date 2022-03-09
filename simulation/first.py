import numpy as np
from time import perf_counter
from lib.numerics.algorithms import trapezoidal, vec_midpoint
from lib.utils.plotting import Plotter 
from lib.steepestdescent.sd import SteepestDescent 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
import matplotlib.pyplot as plt

D = 20
N = 1000
v = 1
h = (D/N)
smax = 0.9


functions = [
    lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))
]
S = lambda x, g=0: smax*np.exp(-(np.power(x-D/2, 4)/5000))
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

x = np.linspace(0, D, N)

y_vec = [0]*N
time = 0
i = 0
theta = np.linspace(-np.pi/2, np.pi/2, N)
for gs in functions:
    mid = {}
    times = 0
    print(f"Function nr: {i+1}/{len(functions)}")
    ic = 0
    th = np.arcsin(vec_midpoint(S, 0, D, N)/(v*D))
    g_val = gs(x, th)
    low = vec_midpoint(T1, 0, D, N, g_val)
    print(f"Tid: {low:.3f} Vinkel i grader: {th*180/np.pi:.3f}")
    for x_i in x:
        y_vec[ic] = x_i*np.tan(th) - 1/(v*np.cos(th))*vec_midpoint(S, 0, x_i, N)
        ic += 1

    plt.plot(x, y_vec)
    i += 1
plt.plot([0, D], [0, 0])
plt.show()
