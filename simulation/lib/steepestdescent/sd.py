import numpy as np
from ..numerics.algorithms import trapezoidal, vec_midpoint
from ..utils.plotting import Plotter
import copy

p = Plotter()
class SteepestDescent():

    def __init__(self, x, d, S, T, C, size=10):
        self.x = copy.deepcopy(x)
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
                    tot += c*np.sin((n*np.pi/D)*x)
                    n += 1
                return tot
            
            for c in points:
                tot += c*np.sin((n*np.pi/x[-1])*x)
                n += 1
            return tot
            
        for c in points:
            tot += c*np.sin((n*np.pi/self.d)*self.x)
            n += 1
        return tot

    def time(self, c):
        #return trapezoidal(T1, 0, x[-1], len(x), cosine_expansion(x, x[-1], c))
        return trapezoidal(self.T, 0, self.d, len(self.x), self.cosine_expansion(c))

    def steepest_descent(self, c, learning_rate = 0.5, stopping_threshold = 1e-6):
        nc = len(c)
        h = 0.1
        iterations = 0
        fd = 1
        cold = np.copy(c)
        #while np.absolute(np.sum(cold) - np.sum(c))>= stopping_threshold:
        while fd >= stopping_threshold:
            cold = np.copy(c)
            iterations += 1
            if iterations % 1 == 0:
                self.scatter = np.copy(c)
                self.scatter = np.append(self.scatter, trapezoidal(self.T, 0, self.d, len(self.x), self.cosine_expansion(c)))
                p.plot_scatter(self.scatter)
                p.plot_pause(0.1)
            for i in range(nc):
                fd = (self.time([c[i]+h]) - self.time([c[i]-h]))/2*h
                c[i] = c[i] - learning_rate*fd
        print(f"\nDone with {iterations=}")
        return c

if __name__ == "__main__":
    x = np.linspace(0, 1, 2)
    print(sine_expansion(x, [0, 1]))
