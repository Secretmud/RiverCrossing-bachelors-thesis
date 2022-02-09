import numpy as np
from time import perf_counter
from lib.numerics.algorithms import vec_midpoint
from lib.utils.plotting import plot_single

D = 20
N = 50
v = 1
h = (D/N)
smax = 0.9


functions = [
    lambda x, theta: np.tan(theta) + S(x)/(v*np.cos(theta))
]
S = lambda x, theta=0: smax*np.exp(-np.power((np.power(x, 1.2)-D/1.5), 4)/200)
T1 = lambda x, g: (1+np.power(g, 2))/(np.sqrt((1+np.power(g, 2))*np.power(v, 2) - np.power(S(x), 2))-g*S(x))

i = 1
theta = np.linspace(-np.pi/2, np.pi/2, N)
# This formula turns the theta array to the normal values between 0 and 2pi.
#theta = (2*np.pi + theta) * (theta < 0) + theta*(theta > 0) 

x_vec = np.linspace(0+h/2, D-h/2, N)
import matplotlib.pyplot as plt
fig = plt.figure()
ax = [0]*2
ax[0] = fig.add_subplot(111)
ax[0].plot([0, D], [0, 0], color="pink")
amt = 2
plots = 0
t = 0
for g in functions:
    mid = {}
    times = 0
    print(f"Function nr: {i}/{len(functions)}")
    y_vec = [0]*N
    ic = 0
    low = vec_midpoint(T1, 0, D, N, g, theta[0])
    theta_low = 0
    for th in np.arange(theta.all()):
        m = vec_midpoint(T1, 0, D, N, g, th)
        if m < low:
            low = m
            theta_low = th

    th = np.arcsin(vec_midpoint(S, 0, D, N)/(v*D))
    print(m)
    print(f"Tid: {low:.3f} Vinkel i grader: {th*180/np.pi:.3f}")
    for x in x_vec:
        y_vec[ic] = x*np.tan(th)/(v*np.cos(th))-1/(v*np.cos(th))*vec_midpoint(S, 0, x, N)
        if (t % amt == 0):
            ax[0].scatter(x, y_vec[ic], color="green")
        plt.pause(h/22)
        ic += 1
        t += 1


    i += 1

plt.show()