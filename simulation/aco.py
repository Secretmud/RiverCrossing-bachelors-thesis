import lib.aco.Ant as ant
import lib.aco.Point as p
import lib.utils.plotting as plotter
import numpy as np
import random
import threading
from multiprocessing import Pool
import numba

g = lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))

n = 100
m = 40
D = 20
smax = 0.9
S = lambda x: smax*np.exp(-np.power(x-D/2, 4)/5000)
v = 1

surface = []
for i in range(m):
    tmp = [0]*n
    surface.append(tmp)
dx = D/n
dy = (D/2)/m
theta = [np.arctan(dy/dx),2*np.pi - np.arctan(dy/dx)]
j = 1

for y in range(m):
    i = 1
    for x in range(n):
        surface[y][x] = p.Point(x, y, i*dx, j*dy, v=S(i*dx), pheremone=1)
        i += 1
    j += 1

time = [
    lambda x: dy/(v-S(x)),
    lambda x: (1+g(x, theta[0])**2)*dx/(np.sqrt((1+g(x, theta[0])**2)*v**2-S(x+dx/2)**2)-g(x, theta[0])*S(x+dx/2)),
    lambda x: np.sqrt(v**2-S(x+dx/2)**2)/dx, 
    lambda x: (1+g(x, theta[1])**2)*dx/(np.sqrt((1+g(x, theta[1])**2)*v**2-S(x+dx/2)**2)+g(x, theta[1])*S(x+dx/2)),
    lambda x: dy/(v+S(x))
]

def neighbor(surface, x, y):
    neigh = {0: surface[y + 1][x] if y + 1 < m else None,
             1: surface[y + 1][x + 1] if y + 1 < m and x + 1 < n else None,
             2: surface[y][x + 1] if x + 1 < n else None,
             3: surface[y + 1][x - 1] if y > 0 and x > 0 else None,
             4: surface[y - 1][x] if y > 0 else None
    }
    return neigh

plot = plotter.Plotter()
plot.set_projection("2d")

a_start_x = 0
a_start_y = int(np.floor(m/2)) 
amount_of_ants = 50

coordinates = ['N', 'NE', 'E', 'SE', 'S']

ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]
f = 0
def generate_solution(ant):
    ant.new_path()
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = neighbor(surface, curr.x, curr.y)
        pheremone = 0
        if (len(neigh) > 0):
            for k, val in neigh.items():
                if val is not None:
                    if neigh[k] not in ant.get():
                        pheremone += val.p
            nxt = random.random()
            potential_nodes = {}
            for k, val in neigh.items():
                if val is not None:
                    if neigh[k] not in ant.get():
                        if v > S(neigh[k].dx):
                            potential_nodes[k] = val.p/pheremone

            potential_nodes = {k: val for k, val in sorted(potential_nodes.items(), key=lambda item: item[1])}

            prev_v = 0
            next_node = 0
            last_key = list(potential_nodes.keys())[-1]
            for k, val in potential_nodes.items():
                if prev_v <= nxt < val:
                    next_node = k
                    break
                if k == last_key:
                    next_node = k

                prev_v = val

            ant.add_path(neigh[next_node])
            neigh[next_node].visited = True
            ant.time += time[next_node](curr.dx)
        else:
            break
        curr = ant.get_current()
    while curr.y != a_start_y:
        if curr.y < a_start_y:
            ant.add_path(surface[curr.y+1][curr.x])
            ant.time += time[0](curr.dx)
        else:
            ant.add_path(surface[curr.y-1][curr.x])
            ant.time += time[-1](curr.dx)
        curr = ant.get_current()


rho = 0.5

def update_pheremones():
    for y in range(m):
        for x in range(n):
            if surface[y][x].visited == True:
                L = 0
                for ant in ants:
                    ant_path = ant.get()
                    last = ant_path[-1]
                    dist = np.sqrt((last.dy - a_start_y)**2 + (last.dx - D)**2)
                    if dist == 0:
                        L += ant.time if surface[y][x] in ant_path else 0
                    else:
                        if x+1 == n and ant.get_current().dy != a_start_y:
                            L = 0
                        else:
                            L += 1/(dist + ant.time) if surface[y][x] in ant_path else 0
                surface[y][x].p = (1-rho)*surface[y][x].p + L
                surface[y][x].visited = False
            else:
                surface[y][x].p = (1-rho)*surface[y][x].p
iterations = 500
plotting = True
if plotting:
    plot.plot_ant_surface([0, D], [-D, D])
    plot.plot_ant([10, D], [a_start_y, a_start_y], clean=True)
while f < iterations:
    if f > 0 and plotting:
        plot.plot_ant_clear()
        plot.plot_ant_surface([0, D], [-D, D])
        plot.plot_ant([0, D], [a_start_y, a_start_y], clean=True)

    p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
    for t in p:
        t.start()
    for t in p:
        t.join()
    if plotting:
        for ant in ants:
            posx = []
            posy = []
            for a in ant.get():
                posx.append(a.dx)
                posy.append(a.dy)
            plot.plot_ant(posx, posy)
            plot.plot_pause(0.01)

    print("xxx")
    update_pheremones()
    if f + 1 < iterations:
        for ant in ants:
            ant.time = 0
    f += 1
    print(f"{f}/{iterations}")

times = []

for a in ants:
    times.append(a.time)
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant(X, Y)

plot.plot_show()
print(sorted(times))