import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from numba import njit


def plot_image(y, fig_name):
    """
    Plot the segmented image
    """

    plt.figure(figsize=(10, 8))
    plt.imshow(y, cmap="nipy_spectral_r")
    plt.colorbar()
    plt.axis("off")
    plt.savefig(fig_name)
    plt.show()


@njit
def local_energy(pixel_proba):
    """
    Local energy of a given pixel with respect to a class c
    """

    return -np.log((1 / pixel_proba) - 1) / 4


def hamiltonian(lattice_size, beta, probabilities):
    """
    Calculate the Hamiltonian of a GIVEN state
    """

    external_field = {}
    neighbors_coupling = {}

    for i in range(lattice_size):
        for j in range(lattice_size):

            spin = i * lattice_size + j
            external_field[spin] = -local_energy(probabilities[spin][0] + 0.0000001)

            neighbors_indexes = [
                [(i + 1) % lattice_size, j],
                [(i - 1) % lattice_size, j],
                [i, (j + 1) % lattice_size],
                [i, (j - 1) % lattice_size],
            ]

            for k in range(len(neighbors_indexes)):
                neighbor = (
                    neighbors_indexes[k][0] * lattice_size + neighbors_indexes[k][1]
                )
                neighbors_coupling[(spin, neighbor)] = -beta

    return external_field, neighbors_coupling
