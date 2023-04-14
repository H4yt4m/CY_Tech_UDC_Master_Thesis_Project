# Credits :
# https://www.youtube.com/watch?v=nnw0Xlbj3JM
# https://rajeshrinet.github.io/blog/2014/ising-model/

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import sys
import json
import math
import matplotlib.animation as animation
import copy
from functools import partial
import os
import time

# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Get experiment values from parameters file."
    )
    if sys.argv[1] == "--generate":
        parser.add_argument(
            "--generate",
            type=str,
            help="Add the parameters file to generate the lattice",
        )
        args = parser.parse_args()
        file = open(args.generate, "r")
        parameters_file_path = json.load(file)
        file.close()
        return parameters_file_path
    else:
        print("\nMode not recognized.")


def initialise_config(lattice_size, probabilities=None):
    # # Option 1 : Random initialisation
    # lattice = 2*np.random.randint(2, size=(lattice_size,lattice_size))-1

    # Option 2 : Initialisation based on threshholding from the prbabilities
    if probabilities is None:
        print(
            "\n\nPlease specify the file containing the probabilities to initialise the lattice.\n\n"
        )
    else:
        lattice = np.zeros(shape=(lattice_size, lattice_size))
        for i in range(lattice_size):
            for j in range(lattice_size):
                lattice[i][j] = (
                    -1 if probabilities[i * lattice_size + j][0] < 0.5 else 1
                )

    return lattice


def neighbours(lattice, x, y):
    neighbors = []
    lattice_size = len(lattice[0])

    # Get general indices of neighbours
    neighbors_x = [x - 1, x, x, x + 1]
    neighbors_y = [y, y - 1, y + 1, y]

    # To avoid out index out of range when updating the arrays
    offset = 0

    # Check if the neighbor pixel exists
    for k in range(4):
        if not (
            0 < neighbors_x[k - offset] < lattice_size
            and 0 < neighbors_y[k - offset] < lattice_size
        ):
            neighbors_x.pop(k - offset)
            neighbors_y.pop(k - offset)
            offset += 1

    for k in range(len(neighbors_x)):
        neighbors.append(lattice[neighbors_x[k], neighbors_y[k]])

    return neighbors


# Local energy of a given pixel with respect to a class c
def local_energy(pixel_proba):
    return -np.log((1 / pixel_proba) - 1) / 4


def hamiltonian(lattice, beta, probabilities):
    # This is the hamiltonian of a GIVEN state
    # This is NOT the change of energy !

    external_field = 0
    neighbors_coupling = 0
    lattice_size = len(lattice[0])

    # Energy from the total magnetic field present
    for i in range(lattice_size):
        for j in range(lattice_size):
            # get one spin at a time from all spins in the lattice
            external_field += (
                -local_energy(probabilities[i * lattice_size + j][0] + 0.0000001)
                * lattice[i, j]
            )

    # Energy from the neighbors
    for i in range(1, lattice_size - 1):
        for j in range(1, lattice_size - 1):
            # One spin at a time from all spins in the lattice

            # Neighbors of the CURRENT spin
            neighbors = neighbours(lattice, i, j)

            # Calculate the coupling-related energy
            for k in range(len(neighbors)):
                neighbors_coupling += -beta * lattice[i, j] * neighbors[k]

    return external_field + neighbors_coupling


# Cost of spin flip
def state_transition_probability(delta_hamiltonians, beta):
    return np.exp(-beta * delta_hamiltonians)


# To verify
def pixel_proba_post_ising(list_lowest_energy_configurations, pixel_x, pixel_y):
    K = len(list_lowest_energy_configurations)

    # Canonical partition, ie. normalization constant
    canonical_partition = 0
    for eps in range(K + 1):
        lattice = list_lowest_energy_configurations[eps]
        canonical_partition += np.exp(-hamiltonian(lattice, beta, probabilities))

    # Pixel probability
    for k in range(K + 1):
        lattice = list_lowest_energy_configurations[k]
        spin = lattice[pixel_x][pixel_y]
        acc += (1 if spin == 1 else 0) / np.exp(
            hamiltonian(list_lowest_energy_configurations[k], beta, probabilities)
        )

    pixel_proba = acc / canonical_partition

    return pixel_proba


def generate_frames(nb_candidate_pixels, probabilities, beta, config):
    lattice_size = len(config[0])

    for _ in range(nb_candidate_pixels):
        # Pick a random spin
        spin_x = np.random.randint(0, lattice_size)
        spin_y = np.random.randint(0, lattice_size)

        # Flip the chosen spin in the candidate config
        candidate_config = copy.deepcopy(config)
        candidate_config[spin_x, spin_y] *= -1

        # Calculate energy change between the two configs
        delta_hamiltonians = hamiltonian(
            candidate_config, beta, probabilities
        ) - hamiltonian(config, beta, probabilities)

        # Test whether we accept the flip or not
        if delta_hamiltonians <= 0 or np.random.uniform(
            0.0, 1.0
        ) < state_transition_probability(delta_hamiltonians, beta):
            config = copy.deepcopy(candidate_config)

    return config


def main():
    frames_list = []

    try:
        # Parse experiment parameters
        args = parse_arguments()
        lattice_size = args.get("lattice_size")
        max_iterations = args.get("max_iterations")
        beta = args.get("beta")
        s = args.get("seed")
        nb_candidate_pixels = args.get("nb_candidate_pixels")
        visualize_or_save = args.get("visualize_or_save")

        np.random.seed(s)

    except:
        print(
            "\nPlease choose an execution mode :\n -> For generating a new Ising model, please add : --generate [PARAMETERS_FILE_PATH] \n\n"
        )

    # Initiate matplotlib elements
    fig, ax = plt.subplots()
    probabilities = np.loadtxt("probabilities.txt", dtype=float, delimiter=" ")

    frames_list.append(initialise_config(lattice_size, probabilities))

    # Generate frames
    start = time.time()
    for i in range(max_iterations - 1):
        # At each iteration i, we generate the next state based on the state
        # at step i, ie. the saved state in frames_list[i]
        frames_list.append(
            generate_frames(nb_candidate_pixels, probabilities, beta, frames_list[i])
        )
    elapsed = time.time() - start

    ims = []

    # Initialise the figure
    ax.imshow(frames_list[0])

    # Generate the animations for the figure
    for i in range(1, max_iterations):
        im = ax.imshow(frames_list[i], animated=True)
        ims.append([im])

    # Animate the figure
    anim = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat_delay=1000)

    # Visualize lattice interactively
    if visualize_or_save == "visualize":
        plt.show()

    # Save animation as mp4 file
    elif visualize_or_save == "save":

        # Format : gif
        f = r"./ising_model.gif"
        writergif = animation.PillowWriter(fps=60)
        anim.save(f, writer=writergif)

        # # Format : mp4 (Option 1 : after generating a gif)
        # os.system(
        #     'ffmpeg -y -i ising_model.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ising_model.mp4'
        # )

        # # Format : mp4 (Option 2 : without generating a gif)
        # anim.save("ising_model.mp4")

    print(
        "\n\n Elapsed wall-clock time to generate the frames is {}s\n\n".format(elapsed)
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
