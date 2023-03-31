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

# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Get experiment values from parameters file.')
    if sys.argv[1] == "--generate" :
        parser.add_argument('--generate', type=str, help='Add the parameters file to generate the lattice')
        args = parser.parse_args()
        parameters_file_path = json.load(open(args.generate))
        return parameters_file_path   
    # elif sys.argv[1] == Other modes ?
    else :
        print("\nMode not recognized.")

def initialise_config(lattice_size):
    return 2*np.random.randint(2, size=(lattice_size,lattice_size))-1

def get_neighbours(config, x, y):
    return [config[x+1,y], config[x-1,y], config[x,y+1], config[x,y-1]]

# Local energy of a given pixel with respect to a class c
def calculate_local_energy(pixel_proba):
    return -np.log((1/pixel_proba)-1)/4

def calculate_hamiltonian(lattice, lattice_size, beta):
    # This is the hamiltonian of a GIVEN state
    # This is NOT the change of energy ! 

    external_field_term = 0
    coupling_term = 0

    # Todo : Replace by pixels probabilities from SVM
    pixel_proba = 0.99

    # Energy from the total magnetic field present
    for i in range(lattice_size):
        for j in range(lattice_size):
            # get one spin at a time from all spins in the lattice
            external_field_term += -calculate_local_energy(pixel_proba) * lattice[i, j]

    # Energy from the neighbors
    for i in range(1, lattice_size-1):
        for j in range(1, lattice_size-1):
            # One spin at a time from all spins in the lattice

            # Neighbors of the CURRENT spin
            neighbors = get_neighbours(lattice, i, j)

            # Calculate the coupling-related energy
            for k in range (4) :
                coupling_term += -beta * lattice[i,j] * neighbors[k]

    return external_field_term + coupling_term

# Cost of spin flip
def state_transition_probability(delta_hamiltonians, beta):
    return np.exp(-beta * delta_hamiltonians)

# Simulation function
def simulate(nb_candidate_pixels_per_iteration):
    global config
    lattice_size = len(config[0])

    for _ in range(nb_candidate_pixels_per_iteration):
        # Pick a random spin
        spin_x = np.random.randint(0, lattice_size)
        spin_y = np.random.randint(0, lattice_size)

        # Flip the chosen spin in the candidate config
        candidate_config = config
        candidate_config[spin_x, spin_y] *= -1

        # Calculate energy change between the two configs
        delta_hamiltonians = calculate_hamiltonian(candidate_config, lattice_size, beta) -\
            calculate_hamiltonian(config, lattice_size, beta) 

        # Test whether we accept the flip or not
        if delta_hamiltonians < 0 :
        # if np.random.randint(0, 1) < state_transition_probability(delta_hamiltonians, beta):
            config[spin_x, spin_y] *= -1    

# Visualisation
def init():
    im.set_data(config)
    return im,

def animate(i):
    simulate(1)
    im.set_data(config)
    return im,

try:
    # Parse experiment parameters
    args = parse_arguments()
    lattice_size = args.get("lattice_size")
    J = args.get("J")
    max_iterations = args.get("max_iterations")
    beta = args.get("beta")
    s = args.get("seed")

    np.random.seed(s)

except:
    print("\nPlease choose an execution mode :\n -> For generating a new Ising model : --generate PARAMETERS_FILE_PATH \n -> For ???")

try:
    # Visualize lattice
    fig = plt.figure()
    config = initialise_config(lattice_size)
    im = plt.imshow(config)
    anim = animation.FuncAnimation(fig, animate, frames=200, interval=1, blit=True)
    plt.show()
    # anim.save('ising_model.gif')

except:
    print("\nError visualizing Ising model.")