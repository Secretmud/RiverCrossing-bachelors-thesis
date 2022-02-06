import matplotlib.pyplot as plt

def plot_single(x, y, x1, y1):
    plt.plot(x, y)
    plt.plot(x1, y1, "r+")
    plt.xlabel("X-akse, theta")
    plt.ylabel("Y-akse, tid")
    plt.show()