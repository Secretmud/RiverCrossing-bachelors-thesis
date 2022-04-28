import lib.aco.Ant as ant
import lib.aco.Point as p
import lib.utils.plotting as plotter
import numpy as np
import random
import threading
g = lambda x, theta: np.tan(theta) - S(x)/(v*np.cos(theta))

iterations = 9000
plotting = True
plotting_interval = 2
amount_of_ants = 100
n_alpha = 1
n_beta = 1
rho = 0.5
alpha = 0.01
elite = int(amount_of_ants/2)
n = 300
m = 3*n
D = 20
W = 20
smax = 0.9
S = lambda x: smax*np.exp(-np.power(x-D/2, 4)/5000)
v = 1

surface = []
for i in range(m):
    tmp = [0]*n
    surface.append(tmp)
dx = D/n
dy = W/m
theta = [
    np.arctan(dy/dx),
    2*np.pi - np.arctan(dy/dx)
]
j = 1

a_start_x = 0
a_start_y = 0
for y in range(m):
    i = 1
    for x in range(n):
        c_dy = (-W/2)+j*dy
        surface[y][x] = p.Point(x, y, i*dx, c_dy, pheremone=1)
        if c_dy == 0:
            a_start_y = y

        i += 1
    j += 1
# New SE and NE functions
time = [
    lambda x, y: dy/(v+S(x)),
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(dy/dx)**2) + dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dx/np.sqrt(v**2-S(x+dx/2)**2), 
    lambda x, y: dx/v*(np.sqrt(1-(S(x+dx/2)/v)**2+(dy/dx)**2) - dy/dx*(S(x+dx/2)/v))/(1-(S(x+dx/2)/v)**2),
    lambda x, y: dy/(v-S(x))
]

def neighbor(surface, x, y):
    if v > S((x+1)*dx):
        neigh = {
                #0: surface[y + 1][x] if y + 1 < m else None,                       # North
                1: surface[y + 1][x + 1] if y + 1 < m and x + 1 < n else None,     # North East
                2: surface[y][x + 1] if x + 1 < n else None,                       # East
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n else None,         # South East
                #4: surface[y - 1][x] if y > 0 else None                            # South
        }
    else:
        neigh = {
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n else None,         # South East
                #4: surface[y - 1][x] if y > 0 else None                            # South
        }

    return {k: v for k, v in neigh.items() if v is not None}

for y in range(m):
    for x in range(n):
        surface[y][x].neigh = neighbor(surface, x, y)

plot = plotter.Plotter()
plot.set_projection("2d")


ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]
f = 0

"""
def generate_solution(ant):
    ant.new_path()
    ant.time = 0
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = curr.neigh
        pheremone = 0
        if (len(neigh) > 0):
            nxt = random.random()
            potential_nodes = {}
            for k, val in neigh.items():
                if neigh[k] not in ant.get():
                    potential_nodes[k] = val.p#+(time[k](neigh[k].dx, neigh[k].dy))
                    pheremone += val.p
            
            for i in potential_nodes.keys():
                potential_nodes[i] /= pheremone
            

            potential_nodes = {k: val for k, val in sorted(potential_nodes.items(), key=lambda item: item[1])}

            #print(f"{potential_nodes}")

            prev_val = 0
            for k, val in potential_nodes.items():
                potential_nodes[k] = val + prev_val
                prev_val += val
            
            #print(f"{potential_nodes}")

            prev_v = 0
            next_node = 0
            last_key = list(potential_nodes.keys())[-1]
            for k, val in potential_nodes.items():
                if k == last_key:
                    next_node = k
                    break
                if prev_v <= nxt <= val:
                    next_node = k
                    break

                prev_v = val

            #print(f"{neigh} {next_node}")
            ant.add_path(neigh[next_node])
            neigh[next_node].visited = True
        else:
            break
        curr = ant.get_current()
        ant.time += time[next_node](curr.dx, curr.dy)
    edged = False
    k = 0
    while curr.y != a_start_y:
        if k == 0:
            edged = True
            ant.last_dy = curr.dy
            k += 1
        if curr.y < a_start_y:
            ant.add_path(surface[curr.y+1][curr.x])
            curr = ant.get_current()
            ant.time += 2*time[0](curr.dx, curr.dy)
        else:
            ant.add_path(surface[curr.y-1][curr.x])
            curr = ant.get_current()
            ant.time += 2*time[-1](curr.dx, curr.dy)
    
    ant.edged = edged

"""
def generate_solution(ant):
    ant.new_path()
    ant.time = 0
    curr = ant.get_current()
    while curr.x + 1 != n:
        neigh = curr.neigh
        pheremone = 0
        if (len(neigh) > 0):
            potential_nodes = {}
            for k, val in neigh.items():
                potential_nodes[k] = float(val.p**n_alpha)#*float((time[k](neigh[k].dx, neigh[k].dy))**n_beta)
                pheremone += potential_nodes[k]

            nxt = random.random()
            potential_nodes = {k: val for k, val in sorted(potential_nodes.items(), key=lambda item: item[1])}

            #print(f"{potential_nodes}")

            prev_val = 0
            for k, val in potential_nodes.items():
                potential_nodes[k] = val + prev_val
                prev_val += val
            
            #print(f"{potential_nodes}")

            prev_v = 0
            next_node = 0
            last_key = list(potential_nodes.keys())[-1]
            for k, val in potential_nodes.items():
                if k == last_key:
                    next_node = k
                    break
                if prev_v <= nxt <= val:
                    next_node = k
                    break

                prev_v = val
                """
            prev_v = 0
            next_node = 0
            for k, val in potential_nodes.items():
                weigth = val / pheremone
                if nxt <= weigth + prev_v:
                    next_node = k
                    break

                prev_v = weigth
                """

            ant.add_path(neigh[next_node])
        else:
            break
        curr = ant.get_current()
        ant.time += time[next_node](curr.dx, curr.dy)
    while curr.y != a_start_y:
        if curr.y < a_start_y:
            ant.add_path(surface[curr.y+1][curr.x])
            curr = ant.get_current()
            ant.time += 2*time[0](curr.dx, curr.dy)
        else:
            ant.add_path(surface[curr.y-1][curr.x])
            curr = ant.get_current()
            ant.time += 2*time[-1](curr.dx, curr.dy)
    


"""
Update the pheremones for each point that has been hit by an ant. 
"""



def update_pheremones(best_ants=ants):
    print(len(best_ants))
    pheremone = []
    global alpha
    for i in range(m):
        tmp = [0]*n
        pheremone.append(tmp)

    for ant in best_ants:
        for p in ant.get():
            pheremone[p.y][p.x] += ant.time
    
    for y in range(m):
        for x in range(n):
            diff = surface[y][x].neigh
            tot_diff = 0
            for k, val in diff.items():
                tot_diff += val.p
            surface[y][x].p = (1-rho)*surface[y][x].p+(pheremone[y][x] + alpha*tot_diff)
"""
def update_pheremones(best_ants=ants):
    print(f"Number of elite ants: {len(best_ants)}")
    ant_pheremone = np.zeros((m,n))
    for ant in best_ants:
        for p in ant.get():
            ant_pheremone[p.y][p.x] += 1/ant.time
    
    for y in range(m):
        for x in range(n):
            surface[y][x].p = (1-rho)*surface[y][x].p + ant_pheremone[y][x]
"""

if plotting:
    plot.plot_ant_surface([0, D], [-10, 10])
from alive_progress import alive_bar
import operator
i = 0
import statistics
sd = []
mean = []
with alive_bar(iterations) as bar:
    old_sum = 0
    while i < iterations:
        if i > 0 and plotting:
            plot.plot_ant_clear()
            plot.plot_ant_surface([0, D], [-10, 10])

        p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
        for t in p:
            t.start()
        for t in p:
            t.join()
        if plotting and i%plotting_interval == 0:

            """
            x = np.linspace(0, D, n)
            y = np.linspace(-10, 10, m)
            z = np.zeros((m,n))
            for j in range(m):
                for i in range(n):
                    z[j][i] = surface[j][i].p
            plot.plot_scatter_std(x, y, z)
            plot.plot_pause(1/amount_of_ants)
            """
            for ant in ants:
                posx = []
                posy = []
                for a in ant.get():
                    posx.append(a.dx)
                    posy.append(a.dy)
                plot.plot_ant(posx, posy)
                plot.plot_pause(1/amount_of_ants)
        times = {}
        for ant in ants:
            times[ant] = ant.time
        times = sorted(times.items(), key=operator.itemgetter(1))[:elite]
        best_ants = []
        times_ant = []
        for ant in ants:
            times_ant.append(ant.time)
        for k in times:
            best_ants.append(k[0])
        times_ant.sort()
        print(f"{times_ant[0]} {abs(old_sum - sum(times_ant))}")
        sd.append(statistics.stdev(times_ant))
        mean.append(statistics.mean(times_ant))
        if abs(old_sum - sum(times_ant)) < 10e-6:
            for val1, val2 in zip(ants, times_ant):
                val1.time = val2

            break
        old_sum = sum(times_ant)
        update_pheremones(best_ants=best_ants)
        bar()
        i += 1


times = []

for a in ants:
    times.append(a.time)
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-2, surface[a_start_y][a_start_x].dy+2])
    plot.plot_ant(X, Y)

with open(f"sd/{rho}_{alpha}_{m}_{n}_size({len(sd)}).txt", "w+") as f:
    for s in sd:
        f.write(f"{s},")
    f.write("\n")
    for m in mean:
        f.write(f"{m},")

plot.plot_show()
print(sorted(times))
print(sd)