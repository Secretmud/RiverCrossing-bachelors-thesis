from jax import grad, jit
import jax.numpy as jnp
import time
import matplotlib as mpl
import matplotlib.pyplot as plt



def main(func):
    i = 0
    t = 0
    grad_tanh = jit(grad(func,(i, t)), backend="gpu")  # Obtain its gradient function
    start = time.time()
    while i < 1000:
        i = i + 0.0
        grad_tanh(i, t)   # Evaluate it at x = 1.0
        i += 1
        t += 0.01

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);  # Plot some data on the axes.
    plt.show()

    print(f"The calculation took: {time.time() - start}s")