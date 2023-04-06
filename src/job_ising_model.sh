#!/bin/bash

#SBATCH -J ising_job            # Job name
#SBATCH -o ising_job_%j.o       # Name of stdout output file(%j expands to jobId)
#SBATCH -e ising_job_%j.e       # Name of stderr output file(%j expands to jobId)
#SBATCH -c 1                    # Cores per task requested
#SBATCH -t 00:10:00             # Run time (hh:mm:ss)
#SBATCH --mem-per-cpu=1G        # Memory per core demandes

module load cesga/2020
python3 ./ising_model.py --generate ./param_file.json 