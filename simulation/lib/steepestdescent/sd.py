import numpy as np
from ..numerics.algorithms import trapezoidal, vec_midpoint
from ..utils.plotting import Plotter
import copy

p = Plotter()
class SteepestDescent():

    def __init__(self, x, d, S, T, C, size=10):
        self.x = np.copy(x)
        self.d = d
        self.S = S
        self.T = T
        self.c = C
        self.size = size
        self.scatter = 0


    def cosine_expansion(self, points, x=None, D=None):
        tot = 0.0 
        n = 1
        if x is not None:
            if D is not None:
                for c in points:
                    tot += c*np.cos((n*np.pi/D)*x)
                    n += 1
                return tot
            
            for c in points:
                tot += c*np.cos((n*np.pi/x[-1])*x)
                n += 1
            return tot
            
        for c in points:
            tot += c*np.cos((n*np.pi/self.d)*self.x)
            n += 1
        return tot

    def time(self, c):
        #return trapezoidal(T1, 0, x[-1], len(x), cosine_expansion(x, x[-1], c))
        return trapezoidal(self.T, 0, self.d, len(self.x), self.cosine_expansion(c))

    def steepest_descent(self, c, plot=False, learning_rate = 1, stopping_threshold = 1e-6):
        nc = len(c)
        h = 0.1
        iterations = 0
        fd = 1
        cold = [0.01]*len(c)
        #while >= stopping_threshold:
        while np.absolute(np.sum(cold) - np.sum(c)) >= stopping_threshold:
            cold = np.copy(c)
            iterations += nc
            if plot:
                if iterations % 1 == 0:
                    self.scatter = np.copy(c)
                    self.scatter = np.append(self.scatter, trapezoidal(self.T, 0, self.d, len(self.x), self.cosine_expansion(c)))
                    #p.plot_scatter_3d(self.scatter)
                    p.plot_scatter_3d(self.scatter)
            for i in range(nc):
                minc = np.copy(c)
                posc = np.copy(c)
                minc[i] = minc[i] - h
                posc[i] = posc[i] + h
                fd = (self.time(posc) - self.time(minc))/2*h
                c[i] = c[i] - learning_rate*fd
            print(f"{iterations=}", end="\r")
        print(f"\nDone with {iterations=}")
        return c

