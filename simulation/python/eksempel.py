from math import asin, exp, sqrt

def trapezoidal(f, start, end, n):
    h = float(end - start) / n
    section = 0.0
    section += f(start)/2.0
    for i in range(1, n):
        section += f(start + i*h)
    section += f(end)/2.0
    return section * h

v = 1
D = 20
smax = .9

N = 1000

S = lambda x: smax*exp(-pow((x-D/2), 4)/5000)

T1int = lambda x: 1/sqrt(pow(v, 2) - pow(S(x), 2))

T1 = trapezoidal(T1int, 0, D, N)

I = trapezoidal(S, 0, D, N)

theta = asin(I/(v*D))

T2 = pow(D, 2)/(sqrt(pow((v*D), 2) - pow(I, 2)))

print(f"Strat1: {T1} Start2: {T2}")