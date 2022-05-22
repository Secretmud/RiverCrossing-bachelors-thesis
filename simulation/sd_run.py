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
smax = 0.2

p = Plotter()
plot = False
if plot:
    p.set_projection("3d")
else:
    p.set_projection("2d")

S = lambda x: smax*np.exp(-(np.power(x-D/2, 4)/5000))
#S = lambda x: smax*np.power(x, 0)
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))
tests = [50]
i = 0
for test in tests:
    smax = 0.9
    Nt = test
    N = 100*Nt
    x = np.linspace(0, D, N)
    c_start = [0]*Nt
    sd = SteepestDescent(x, D, S, T1, c_start)



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
        p.plot_surface(C1, C2, z, i)
        #p.plot_contour(C1, C2, z)
        p.plot_clear()
        i += 1
    points = sd.steepest_descent(c_start, plot=plot)
    time_taken = trapezoidal(T1, 0, D, N, sd.cosine_expansion(points))
    print(points)
    if plot:
        points.append(time_taken)
        p.plot_scatter_3d(points, "last")
        print(points)
    if not plot:
        n = 1
        tot = 0
        for c in points:
            tot += (c*D)/(n*np.pi)*np.sin(n*np.pi*x/D)
            n += 1

        plt.plot(x, tot, label=f"{test} sine expansions")
        print(time_taken)

functions = [
    lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))
]

plt.plot([0, D], [0, 0], label="Straight across")
plt.xlim([0, D])
plt.xlabel("River")
plt.ylabel("Shore")

if not plot:
    plt.plot(x, S(x), label="Current")
    y_vec = [0]*N
    i = 0
    theta = np.linspace(-np.pi/2, np.pi/2, N)
    for gs in functions:
        print(f"Function nr: {i+1}/{len(functions)}")
        ic = 0
        th = np.arcsin(trapezoidal(S, 0, D, N)/(v*D))
        g_val = gs(x, th)
        low = trapezoidal(T1, 0, D, N, g_val)
        print(f"Tid: {low:.3f} Vinkel i grader: {th*180/np.pi:.3f}")
        for x_i in x:
            y_vec[ic] = x_i*np.tan(th) - 1/(v*np.cos(th))*trapezoidal(S, 0, x_i, N)
            ic += 1

        plt.plot(x, y_vec, label="Semi analytic", linestyle="dashed")
        i += 1

    plt.legend(loc="upper right")

p.plot_show()