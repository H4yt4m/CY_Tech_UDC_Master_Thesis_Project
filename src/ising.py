# https://rajeshrinet.github.io/blog/2014/ising-model/
# https://itp.uni-frankfurt.de/~mwagner/teaching/C_WS19/projects/Ising_proj.pdf
# https://tanyaschlusser.github.io/posts/mcmc-and-the-ising-model/

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import sys
import json

def read_image(folder_path):
    return mpimg.imread(folder_path + 'img.jpg')

def rgb_to_grey_image(img):
    return np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])

def reshape_image(img, square_length):
    return img[0:square_length, 0:square_length]

def normalize_image(img):
    normalized_img = np.empty(img.shape)
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            normalized_img[i,j] = img[i,j]/255
    return normalized_img

def default_preprocess_img(path):
    temp1 = read_image(path)
    temp2 = rgb_to_grey_image(temp1)
    temp3 = reshape_image(temp2, 300)
    return normalize_image(temp3)

def parse_arguments():
    parser = argparse.ArgumentParser()
    if sys.argv[1] == "--generate" :
        parser.add_argument('--generate', dest='parameters_file_path', type=str, help='Add the configuration file to generate the lattice')
        args = json.load(open(parameters_file_path))
        return args   
    # elif sys.argv[1] == some other mode ?
    else :
        print("Mode not recognized.")
        return 0;

def get_neighbours(config, x, y):
    return [config[x+1,y], config[x-1,y], config[x,y+1], config[x,y-1]]

def split_train_test(data):
    # todo
    return train, test

def split_train(train):
    #todo
    return pixel_class, other_classes

def binary_svm_classifier(img):
    # todo
    return 0

def calculate_probabilities(data, x, y):
    # todo
    return 0

def calculate_local_energy(pixel_proba):
    return -log((1/pixel_proba)-1)/4

def calculate_hamiltonian(configuration, x, y, beta):
    # todo
    return 0

def step(configuration, beta):
    x = np.random.randint(0, configuration.shape(0))
    y = np.random.randint(0, configuration.shape(1))
    cost = calculate_hamiltonian(configuration, x, y, beta)
    if (cost < 0) or (rand() < np.exp(-cost*beta)):	
        configuration[x, y] *= -1
    return configuration

def simulate():
    args = parse_arguments();
    input_path = args.get("input_path")
    output_path = args.get("output_path")
    max_iterations = args.get("max_iterations")
    beta = args.get("max_iterations")
    config = default_preprocess_img('img.jpg')
    plt.imshow(config)
    for i in range(max_iterations):
        step(config, beta)
        if i == 1:       configPlot(f, config, i, N, 2);
        if i == 4:       configPlot(f, config, i, N, 3);
        if i == 32:      configPlot(f, config, i, N, 4);
        if i == 100:     configPlot(f, config, i, N, 5);
        if i == 300:     configPlot(f, config, i, N, 6);  

simulate()