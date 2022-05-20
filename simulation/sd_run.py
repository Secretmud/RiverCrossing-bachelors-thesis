import numpy as np
from time import perf_counter
from lib.numerics.algorithms import trapezoidal
from lib.utils.plotting import Plotter 
from lib.steepestdescent.sd import SteepestDescent 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
import matplotlib.pyplot as plt

D = 20
v = 1
smax = 0.9

p = Plotter()
p.set_projection("2d")
S = lambda x: smax*np.exp(-(np.power(x-D/2, 4)/5000))
#S = lambda x: smax*np.power(x, 0)
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))
tests = [2, 12, 25, 50]
for test in tests:
    Nt = test
    N = 100*Nt
    x = np.linspace(0, D, N)
    c_start = [0]*Nt
    sd = SteepestDescent(x, D, S, T1, c_start)



    plot = False
    if plot:
        C1 = C2 = np.linspace(-40, 40, N)
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
        p.plot_surface(C1, C2, z)
        #p.plot_contour(C1, C2, z)
    points = sd.steepest_descent(c_start, plot=plot)
    time_taken = trapezoidal(T1, 0, D, N, sd.cosine_expansion(points))
    print(points)
    if plot:
        points.append(time_taken)
        p.plot_scatter_3d(points, "last")
        #p.plot_pause(0.005)
        print(points)
    if not plot:
        n = 1
        tot = 0
        for c in points:
            #tot += (c)/(n*np.pi)*np.sin((c)/(n*np.pi))
            tot += (c*D)/(n*np.pi)*np.sin(n*np.pi*x/D)
            #c = (c*D)/(n*np.pi)*np.sin(n*np.pi*x[n-1]/D)
            n += 1

        plt.plot(x, tot, label=f"{test} sine expansions")
        print(time_taken)

plt.plot(x, S(x), label="Current")

plt.legend(loc="upper right")
plt.xlim([0, D])

p.plot_show()