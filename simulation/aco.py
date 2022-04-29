import lib.aco.Ant as ant
import lib.aco.Point as p
import lib.utils.plotting as plotter
import numpy as np
import random
import threading

iterations = 9000
plotting = True
amount_of_ants = 1000
rho = 0.5
alpha = 0
elite = int(amount_of_ants/10)
n = 20
m = 1*n
D = 20
W = 10
smax = 0.9
offset = 5
S = lambda x: smax*np.exp(-np.power(x-D/2, 4)/5000)
v = 1

surface = []
for i in range(m):
    tmp = [0 for i in range(n)]
    surface.append(tmp)
dx = D/n
dy = W/m

a_start_x = 0
a_start_y = 0
def free_flow():
    global a_start_y
    j = 1
    for y in range(m):
        i = 1
        for x in range(n):
            c_dy = (-W/2)+j*dy
            surface[y][x] = p.Point(x, y, i*dx, c_dy, pheremone=1)
            if c_dy == 0:
                a_start_y = y

            i += 1
        j += 1
def force_flow():
    global a_start_y
    j = 1
    for y in range(m):
        i = 1
        for x in range(n):
            c_dy = (-W/2)+j*dy
            c_dx = i*dx
            pheremone = 1
            if abs(c_dy) - dy > D-c_dx:
                pheremone = 0
            surface[y][x] = p.Point(x, y, i*dx, c_dy, pheremone=pheremone)
            if c_dy == 0:
                a_start_y = y

            i += 1
        j += 1


free_flow()
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
                #0: surface[y + 1][x] if y + 1 < m and surface[y + 1][x].p > 0 else None,                       # North
                1: surface[y + 1][x + 1] if y + 1 < m and x + 1 < n and surface[y + 1][x + 1].p > 0 else None,     # North East
                2: surface[y][x + 1] if x + 1 < n and surface[y][x + 1] .p > 0 else None,                       # East
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n and surface[y - 1][x + 1].p > 0  else None,         # South East
                #4: surface[y - 1][x] if y > 0 and surface[y - 1][x].p > 0 else None                            # South
        }
    else:
        neigh = {
                3: surface[y - 1][x + 1] if y > 0 and x + 1 < n and surface[y - 1][x + 1].p > 0 else None,         # South East
                #4: surface[y - 1][x] if y > 0 and surface[y - 1][x].p > 0 else None                            # South
        }

    return {k: v for k, v in neigh.items() if v is not None}
"""
for s in surface:
    for p in s:
        print(f"{p.p}", end=" ")
    print()
exit()
"""
for y in range(m):
    for x in range(n):
        if surface[y][x] is not None:
            surface[y][x].neigh = neighbor(surface, x, y)


plot = plotter.Plotter()
plot.set_projection("2d")


ants = [ant.Ant(surface[a_start_y][a_start_x]) for i in range(amount_of_ants)]
f = 0

"""
generate_solution(ant) -> void
It saves the path the ant has taken inside of the ant object, using the point objects (These are the objects that hold infomation about a specific address in the 2d surface)

The first thing we need to do is set the ant time to 0, this is done for the simple reason that we need store the crossing time for each generation.

We need to know which possible neighboors we have aswell, this is stored inside the point objects, this is done to speed up the code. By doing it this way we only need to 
find the neighboors once. Which is done at the initialization of the surface matrix.

We then create a probability vector and a possible key vector (Used to get the next step using the neighbor dictionary).

We normalize the probability vector based on the sum of all the pheremones we test against.

Then you simply use numpy's random.choice function to get a properly tested discrete probability picker. 

If we dont hit the value of y that doesnt satisfy f(0) = f(D) = 0, we then force the ants to the correct location, this also goes for the x value, which can happen if we use a forced
 flow. 
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
            potential_nodes = []
            selection_probs = []
            for k, val in neigh.items():
                if neigh[k] not in ant.get():
                    selection_probs.append(val.p)
                    potential_nodes.append(k)
                    pheremone += val.p
            
            next_node = 0
            for i in range(len(selection_probs)):
                selection_probs[i] /= pheremone
            next_node = potential_nodes[np.random.choice(len(potential_nodes), p=selection_probs)]
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
    
    while curr.x != n-1:
        ant.add_path(surface[curr.y][curr.x+1])
        curr = ant.get_current()
        ant.time += time[2](curr.dx, curr.dy)
    ant.edged = edged



"""
Update the pheremones for each point that has been hit by an ant. 
"""


def update_pheremones(best_ants=ants):
    print(len(best_ants))
    pheremone = []
    global alpha
    for i in range(m):
        tmp = [0 for i in range(n)]
        pheremone.append(tmp)

    for ant in best_ants:
        for p in ant.get():
            pheremone[p.y][p.x] += 1/ant.time
    
    for y in range(m):
        for x in range(n):
            if surface[y][x] is not None:
                diff = surface[y][x].neigh
                tot_diff = 0
                neighs = 1
                for k, val in diff.items():
                    tot_diff += val.p
                    neighs+=1
                surface[y][x].p = (1-rho)*surface[y][x].p+(pheremone[y][x] + alpha*tot_diff/neighs)
if plotting:
    plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset])
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
            plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset])

        p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
        for t in p:
            t.start()
        for t in p:
            t.join()
        if plotting and i%1 == 0:
            x = np.linspace(0, D, n)
            y = np.linspace(-10, 10, m)
            z = np.zeros((m,n))
            for j in range(m):
                for i in range(n):
                    if surface[j][i] is None:
                        z[j][i] = 0
                    else:
                        z[j][i] = surface[j][i].p
            plot.plot_scatter_std(x, y, z)
            plot.plot_pause(1/amount_of_ants)
        times = {}
        for ant in ants:
            times[ant] = ant.time
        times = sorted(times.items(), key=operator.itemgetter(1))[:elite]
        best_ants = []
        times_ant = []
        f = 1
        for ant in ants:
            times_ant.append(ant.time)
        for k in times:
            k[0].time = 1/f
            best_ants.append(k[0])
            f += 1
        
        times_ant.sort()
        print(f"{times_ant[0]} {times_ant[-1]} {abs(old_sum - sum(times_ant))}")
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
"""
with alive_bar(iterations) as bar:
    for i in range(iterations):
        p = [threading.Thread(target=generate_solution, args=(ant,)) for ant in ants]
        for t in p:
            t.start()
        for t in p:
            t.join()
        update_pheremones()
        if i + 1 != iterations:
            for ant in ants:
                ant.time = 0
        bar()
        
"""


times = []

for a in ants:
    times.append(a.time)
    a = a.get()
    X = []
    Y = []
    for i in a:
        X.append(i.dx)
        Y.append(i.dy)
    plot.plot_ant_surface([0, D], [surface[a_start_y][a_start_x].dy-offset, surface[a_start_y][a_start_x].dy+offset])
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