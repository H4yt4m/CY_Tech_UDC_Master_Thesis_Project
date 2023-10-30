#!/bin/bash

#SBATCH -J ising_job                        # Job name
#SBATCH -o ising_job_%j.o                   # Name of stdout output file(%j expands to jobId)
#SBATCH -e ising_job_%j.e                   # Name of stderr output file(%j expands to jobId)
#SBATCH -c 1                                # Cores per task requested
#SBATCH -t 12:00:00                         # Run time (hh:mm:ss)
#SBATCH --mem-per-cpu=10GB                  # Memory per core demandes
#SBATCH --mail-type=ALL
#SBATCH --mail-user=elmerabeti@cy-tech.fr

module load cesga/2020
pip install numba
python3 ./ising_model.py --generate ./param_file.json 