import numpy as np
from time import perf_counter
from lib.numerics.algorithms import trapezoidal, vec_midpoint
from lib.utils.plotting import Plotter 
from lib.steepestdescent.sd import SteepestDescent 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
import matplotlib.pyplot as plt

D = 20
N = 5000
v = 1
h = (D/N)
smax = 0.9


functions = [
    lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))
]

S = lambda x, g=0: smax*np.exp(-(np.power(x-D/2, 4)/5000))
#S = lambda x: smax*np.power(x, 0)
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

x = np.linspace(0, D, N)
#sd = SteepestDescent(x, D, S, T1, [0])
#print(trapezoidal(T1, 0, D, N, sd.cosine_expansion([-0.6925192930776441, 0.46039340890690966])))
y_vec = [0]*N
time = 0
i = 0
theta = np.linspace(np.pi/2, -np.pi/2, N)
for gs in functions:
    mid = {}
    times = 0
    print(f"Function nr: {i+1}/{len(functions)}")
    ic = 0
    th = np.arcsin(trapezoidal(S, 0, D, N)/(v*D))
    g_val = gs(x, th)
    low = trapezoidal(T1, 0, D, N, g_val)
    """
    for thetas in theta:
        cg_val = gs(x, thetas)
        clow = trapezoidal(T1, 0, D, N, cg_val)
        print(f"{clow} {thetas}")
        if clow < low and 26 < clow < 27:
            low = clow
            th = thetas
    """

    print(f"Tid: {low:.3f} Vinkel i grader: {th*180/np.pi:.3f}")
    for x_i in x:
        y_vec[ic] = x_i*np.tan(th) - 1/(v*np.cos(th))*trapezoidal(S, 0, x_i, N)
        ic += 1

    plt.plot(x, y_vec, label="Path")
    i += 1
plt.plot([0, D], [0, 0], label="Straigh across")
plt.plot(x, S(x), label="Current")
plt.legend(loc="upper right")
plt.xlim([0, D])
plt.xlabel("River")
plt.ylabel("Shore")
plt.show()