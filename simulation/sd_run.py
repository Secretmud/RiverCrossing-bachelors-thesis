import numpy as np
from time import perf_counter
from lib.numerics.algorithms import trapezoidal
from lib.utils.plotting import Plotter 
from lib.steepestdescent.sd import SteepestDescent 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
import matplotlib.pyplot as plt

D = 20
N = 150
v = 1
smax = 0.9

p = Plotter()
S = lambda x, g=0: smax*np.exp(-(np.power(x-D/2, 4)/5000))
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

x = np.linspace(0, D, N)
C1 = C2 = np.linspace(-10, 10, N)
z = np.zeros((N,N), dtype=float)
c_start = [5, 5]
sd = SteepestDescent(x, D, S, T1, c_start)

zi = 0
for ci in range(len(C1)):
    zj = 0
    for cj in range(len(C2)):
        g = sd.cosine_expansion([C1[ci], C2[cj]])
        time = trapezoidal(T1, 0, D, N, g)
        z[zj][zi] = time
        zj += 1
    zi += 1


plot = True
if plot:
    p.set_projection("3d")
    p.plot_surface(C1, C1, z)
points = sd.steepest_descent(c_start)
points.append(trapezoidal(T1, 0, D, N, sd.cosine_expansion(points)))
if plot:
    p.plot_scatter(points, "last")
    p.plot_show()
print(points)
