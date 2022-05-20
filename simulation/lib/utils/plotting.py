import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
from matplotlib.offsetbox import TextArea, VPacker, AnnotationBbox
from matplotlib.colors import LogNorm
import numpy as np


"""
Singleton metaclass, by using this class type we can add to the plots from multiple files without 
sending loads of objects around. The first instance of the class is the only one that gets invoked.
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Plotter(metaclass=Singleton):
    ax = None
    """
    This class containts loads of plotting utility, this should make it easier for us to plot on the fly when we 
    implement ACO. 
    """

    def __init__(self):
        self.dpi = 100
        self.fig = plt.figure(figsize=(1280/self.dpi, 720/self.dpi), dpi=self.dpi)
        self.N = 10
        self.alphas = np.linspace(0.1, 1, self.N)
        self.pathx = [0]*self.N
        self.pathy = [0]*self.N
        self.pathz = [0]*self.N
        self.i = 0
        self.scatter = 0
        self.v = 0
        self.projection = "2d"
        plt.rcParams.update({'font.size': 16})

    def get_projection(self):
        if self.projection == None:
            return "3d"
        else:
            return projection
    
    def set_projection(self, projection):
        self.projection = projection
        if projection == "3d":
            self.ax = self.fig.add_subplot(111, projection=projection)
            self.ax.view_init(elev=54, azim=135)
        else:
            self.ax = self.fig.add_subplot(111)


    def plot_single(self, x, y, x1=None, y1=None, legend=None):
        self.ax.plot(x, y)
        if (x1 != None or y1 != None):
            self.ax.plot(x1, y1, "r+")
        self.ax.set_xlabel("D")
        self.ax.set_ylabel("W")
        if (legend != None):
            posx = min(x) + 2
            posy = max(y) - 5
            Texts = []
            for t in legend:
                Texts.append(TextArea(t))
                texts_vbox = VPacker(children=Texts,pad=0,sep=0)
                ann = AnnotationBbox(texts_vbox,(.02,.5),xycoords=self.ax.transAxes,
                                        box_alignment=(0,.5),bboxprops = 
                                        dict(facecolor='wheat',boxstyle='round'))
            """
            for t in legend:
                print(t)
                ax.text(posx, posy, s=t)
                posy -= 2
            """
            ann.set_figure(self.fig)
            self.fig.artists.append(ann)
        #ax.set_yscale('log')

    def plot_surface(self, X, Y, z):
        Z = np.array(z)
        X, Y = np.meshgrid(X, Y)
        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape
        self.ax.plot_surface(X, Y, Z, cmap='viridis', rcount=rcount, ccount=ccount, facecolors=colors, shade=False, alpha=0.5)
        self.ax.set_xlabel(r"$C_1$", fontsize=12)
        self.ax.set_ylabel(r"$C_2$", fontsize=12)
        self.ax.set_zlabel(r"$T[C_n]$", fontsize=12)

    def plot_contour(self, X, Y, z):
        Z = np.array(z)
        #norm = plt.Normalize(Z.min(), Z.max())
        CS = self.ax.contour(X, 
                             Y, 
                             Z,
                             levels=25
                             )
        #self.ax.set_xlabel(r"$C_1$", fontsize=12)
        #self.ax.set_ylabel(r"$C_2$", fontsize=12)
        self.ax.clabel(CS, inline=True, fmt='%1.1f s', fontsize=10)

    def plot_scatter_3d(self, points, last=None):
        if self.i + 1 == self.N:
            self.ax.plot([self.pathx[0], self.pathx[-1]], [self.pathy[0], self.pathy[-1]])
            self.pathx[0] = self.pathx[-1]
            self.pathy[0] = self.pathy[-1]
            self.pathz[0] = self.pathz[-1]
            self.i = 1
        if self.i == 0:
            for i in range(len(self.pathx)):
                self.pathx[i] = points[0]
                self.pathy[i] = points[1]
                self.pathz[i] = points[2]
            self.scatter = self.ax.scatter(self.pathx, self.pathy, self.pathz, alpha=self.alphas, color="black")
        else:
            self.pathx[self.i] = points[0]
            self.pathy[self.i] = points[1]
            self.pathz[self.i] = points[2]
        if self.i % 1 == 0:
            self.scatter.remove()
            self.scatter = self.ax.scatter(self.pathx, self.pathy, self.pathz, alpha=self.alphas, color="black")
        self.i += 1
        self.fig.savefig(f"animation/{self.v}.png", dpi=self.dpi)
        self.v += 1


    def plot_scatter_2d(self, points, last=None):
        #self.alphas[self.i] = self.alphas[-1]
        if self.i + 1 == self.N:
            self.pathx[0] = self.pathx[-1]
            self.pathy[0] = self.pathy[-1]
            #self.ax.plot(self.pathx, self.pathy)
            self.i = 1
        if self.i == 0:
            for i in range(len(self.pathx)):
                self.pathx[i] = points[0]
                self.pathy[i] = points[1]
            self.scatter = self.ax.scatter(self.pathx, self.pathy, alpha=self.alphas, color="black")
        else:
            self.pathx[self.i] = points[0]
            self.pathy[self.i] = points[1]
        if self.i % 1 == 0:
            self.scatter.remove()
            self.scatter = self.ax.scatter(self.pathx, self.pathy, alpha=self.alphas, color="black")
        self.i += 1
        self.fig.savefig(f"animation/{self.v}.png", dpi=self.dpi)
        self.v += 1

    def plot_show(self):
        plt.show()

    def plot_pause(self, time):
        plt.pause(time)

    def plot_ant(self, X, Y, clean=None):
        if clean:
            self.line = self.ax.plot(X, Y, 'r-')
        else:
            self.line = self.ax.plot(X, Y)

    def plot_ant_surface(self, X, Y, i=None):
        #self.ax.spines['right'].set_visible(False)
        #self.ax.spines['top'].set_visible(False)
        #self.ax.spines['left'].set_visible(False)
        #self.ax.spines['bottom'].set_visible(False)
        plt.xlim(X)
        plt.ylim(Y)
        self.ax.set_xlabel(r"$River$", fontsize=12)
        self.ax.set_ylabel(r"$Shore$", fontsize=12)
        if i is not None:
            self.fig.savefig(f"animation/{i}.png", bbox_inches='tight')

    def plot_ant_clear(self):
        plt.cla()

    def plot_scatter_std(self, x, y, z, i):
        #x, y = np.meshgrid(x, y)
        self.ax.contourf(x, y, z, 20)
        #self.ax.scatter(x, y, s=z)
        self.fig.savefig(f"animation/{i}.png", bbox_inches='tight')

    def plot_quiver(self, x, y, u):
        x, y = np.meshgrid(x, y)
        self.ax.quiver(x, y, u, units='xy')