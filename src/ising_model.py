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


def parse_arguments():
    """
    Parse the parameters of the experiment from the file param_file.json
    """

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


def initialise_lattice(lattice_size, probabilities=None):
    """
    Initialise the lattice for the ising model
    """
    # # Option 1 : Random initialisation
    # lattice = 2 * np.random.randint(2, size=(lattice_size, lattice_size)) - 1

    # Option 2 : Initialisation based on threshholding from the output prbabilities of the svm.
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


@njit
def pixel_neighbors(lattice, x, y):
    """
    Get the neighbours of a given pixel
    Usage of % operator to cycle pixels in the border, so as : The pixel lattice[0,0] is the neighbour of the pixel lattice[0,lattice_size-1]
    """

    lattice_size = len(lattice[0])

    return np.array(
        [
            lattice[(x + 1) % lattice_size, y],
            lattice[(x - 1) % lattice_size, y],
            lattice[x, (y + 1) % lattice_size],
            lattice[x, (y - 1) % lattice_size],
        ]
    )


@njit
def local_energy(pixel_proba):
    """
    Local energy of a given pixel with respect to a class c
    """

    return -np.log((1 / pixel_proba) - 1) / 4


@njit
def hamiltonian(lattice, beta, probabilities):
    """
    Calculate the Hamiltonian of a GIVEN state
    """

    external_field = 0
    neighbors_coupling = 0
    lattice_size = len(lattice[0])

    for i in range(lattice_size):
        for j in range(lattice_size):
            # Get one spin at a time from all spins in the lattice

            # Calculate energy from the total magnetic field present
            external_field += (
                -local_energy(probabilities[i * lattice_size + j][0] + 0.0000001)
                * lattice[i, j]
            )

            # Calculate coupling-related energy from the neighbors
            neighbors = pixel_neighbors(lattice, i, j)

            for k in range(len(neighbors)):
                neighbors_coupling += -beta * lattice[i, j] * neighbors[k]

    return external_field + neighbors_coupling


@njit
def state_transition_probability(delta_hamiltonians, temperature):
    """
    Calculate the cost of spin flip
    """

    return np.exp(-delta_hamiltonians / temperature)


# @njit
# def pixel_proba_post_ising(array_lowest_energy_configurations, pixel_x, pixel_y):
#     """
#     Calculate the new class probability for each pixel, after the quantum annealing
#     """

#     K = len(array_lowest_energy_configurations)

#     canonical_partition = 0

#     for k in range(K + 1):
#         lattice = array_lowest_energy_configurations[k]

#         # Canonical partition, ie. normalization constant
#         canonical_partition += np.exp(-hamiltonian(lattice, beta, probabilities))

#         # Pixel probability
#         spin = lattice[pixel_x][pixel_y]
#         acc += (1 if spin == 1 else 0) / np.exp(
#             hamiltonian(array_lowest_energy_configurations[k], beta, probabilities)
#         )

#     return acc / canonical_partition


@njit
def generate_frames(
    candidate_pixels_per_frame, probabilities, temperature, beta, lattice
):
    """
    Generate the frames to visualize
    """

    lattice_size = len(lattice[0])

    for _ in range(candidate_pixels_per_frame):
        # Pick a random spin
        spin_x = np.random.randint(0, lattice_size)
        spin_y = np.random.randint(0, lattice_size)

        # Flip the chosen spin in the candidate lattice configuration
        candidate_lattice = lattice.copy()
        candidate_lattice[spin_x, spin_y] *= -1

        # Calculate energy change between the two lattices
        delta_hamiltonians = hamiltonian(
            candidate_lattice, beta, probabilities
        ) - hamiltonian(lattice, beta, probabilities)

        # Test whether we accept the flip or not
        if delta_hamiltonians <= 0 or np.random.uniform(
            0.0, 1.0
        ) < state_transition_probability(delta_hamiltonians, temperature):
            lattice = candidate_lattice.copy()

    return lattice


def main():
    """
    Main program
    """

    try:
        # Parse experiment parameters
        args = parse_arguments()
        lattice_size = args.get("lattice_size")
        max_iterations = args.get("max_iterations")
        beta = args.get("beta")
        temperature_min = args.get("temperature_min")
        temperature_max = args.get("temperature_max")
        temperature = (
            temperature_max
            if temperature_min == temperature_max
            else np.linspace(temperature_max, temperature_min, max_iterations)
        )
        s = args.get("seed")
        candidate_pixels_per_frame = args.get("candidate_pixels_per_frame")

        np.random.seed(s)

    except:
        print(
            "\nPlease choose an execution mode :\n -> For generating a new Ising model, please add : --generate [PARAMETERS_FILE_PATH] \n\n"
        )

    # Get the probabilities resulting from the prior SVM
    probabilities = np.loadtxt("probabilities.txt", dtype=float, delimiter=" ")

    # Initialise the array containing the frames
    frames_list = np.empty((max_iterations, lattice_size, lattice_size))
    frames_list[0] = initialise_lattice(lattice_size, probabilities)

    start = time.time()

    # At each iteration i, we generate the next state of the lattice based on the state
    # at step i, ie. the current state in frames_list[i]
    for i in range(max_iterations - 1):
        frames_list[i + 1] = generate_frames(
            candidate_pixels_per_frame,
            probabilities,
            temperature if type(temperature) == float else temperature[i],
            beta,
            frames_list[i],
        )

    # Save the frames in GIF format
    filename = "run99.gif"
    gif = [
        Image.fromarray(np.uint8(f)).convert("RGB").resize((600, 600))
        for f in frames_list
    ]

    gif[0].save(filename, save_all=True, optimize=False, append_images=gif[1:], loop=0)

    elapsed = time.time() - start

    print(
        "\n\n Elapsed wall-clock time to generate the file {} is {}s\n\n".format(
            filename, elapsed
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
