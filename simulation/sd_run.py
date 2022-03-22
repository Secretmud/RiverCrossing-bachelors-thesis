import numpy as np
from time import perf_counter
from lib.numerics.algorithms import trapezoidal
from lib.utils.plotting import Plotter 
from lib.steepestdescent.sd import SteepestDescent 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
import matplotlib.pyplot as plt

D = 20
Nt = 2
N = 10*Nt
v = 1
smax = 0.9

p = Plotter()
S = lambda x: smax*np.exp(-(np.power(x-D/2, 4)/5000))
#S = lambda x: smax*np.power(x, 0)
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

x = np.linspace(0, D, N)
c_start = [9]*Nt
sd = SteepestDescent(x, D, S, T1, c_start)



plot = True
if plot:
    C1 = C2 = np.linspace(-10, 10, N)
    z = np.zeros((N,N), dtype=float)
    zi = 0
    for ci in C1:
        zj = 0
        for cj in C2:
            g = sd.cosine_expansion([ci, cj])
            time = trapezoidal(T1, 0, D, N, g)
            z[zj][zi] = time
            zj += 1
        zi += 1
    p.set_projection("3d")
    p.plot_surface(C1, C1, z)
points = sd.steepest_descent(c_start, plot=plot)
time_taken = trapezoidal(T1, 0, D, N, sd.cosine_expansion(points))
print(points)
if plot:
    points.append(time_taken)
    p.plot_scatter(points, "last")
    p.plot_show()
    print(points)
if not plot:
    n = 1
    tot = 0
    for c in points:
        #tot += (c)/(n*np.pi)*np.sin((c)/(n*np.pi))
        tot += (c*D)/(n*np.pi)*np.sin(n*np.pi*x/D)
        n += 1

    plt.plot(x, tot)
    plt.show()
    print(time_taken)