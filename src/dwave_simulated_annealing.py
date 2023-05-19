import sys
import os
import argparse
import json
import math
import copy
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
from numba import njit
from PIL import Image

from dwave.samplers import SimulatedAnnealingSampler


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
            spin = "S_{}_{}".format(str(i).zfill(3), str(j).zfill(3))

            external_field[spin] = -local_energy(
                probabilities[i * lattice_size + j][0] + 0.0000001
            )

            neighbors_indexes = [
                [(i + 1) % lattice_size, j],
                [(i - 1) % lattice_size, j],
                [i, (j + 1) % lattice_size],
                [i, (j - 1) % lattice_size],
            ]

            for k in range(len(neighbors_indexes)):
                neighbor = "S_{}_{}".format(
                    str(neighbors_indexes[k][0]).zfill(3),
                    str(neighbors_indexes[k][1]).zfill(3),
                )
                neighbors_coupling[(spin, neighbor)] = -beta

    return external_field, neighbors_coupling


def main():
    """
    Main program
    """

    lattice_size = 145
    beta = 0.5

    probabilities = np.loadtxt("probabilities.txt", dtype=float, delimiter=" ")

    external_field, neighbors_coupling = hamiltonian(lattice_size, beta, probabilities)

    sampler_param = {
        "beta_range": [],
        "num_reads": 100,
        "num_sweeps": [],
        "num_sweeps_per_beta": [],
        "beta_schedule_type": ["beta_schedule_options"],
        "seed": [],
        "interrupt_function": [],
        "initial_states": [],
        "initial_states_generator": [],
    }

    start = time.time()

    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample_ising(
        external_field, neighbors_coupling, num_reads=sampler_param["num_reads"]
    )

    print("Elapsed wall time : {} ms".format((time.time() - start) * 100))

    result_sample = sampleset.first.sample
    result_energy = sampleset.first.energy

    clmap = np.array(list(result_sample.values())).reshape(145, 145).astype("float")
    plot_image(clmap, "dwave_simulated_annealing_segmentation.png")

    print("Energy :{}".format(result_energy))
    return 0


if __name__ == "__main__":
    sys.exit(main())
