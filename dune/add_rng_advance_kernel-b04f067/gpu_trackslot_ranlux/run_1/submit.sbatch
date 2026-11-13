#!/bin/bash
#SBATCH --job-name=dune_gpu_trackslot_ranlux_1
#SBATCH --chdir=/home/gqe/Codes/celeritas/analysis/celer_analysis/dune/add_rng_advance_kernel-b04f067/gpu_trackslot_ranlux/run_1
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --partition=hudson
#SBATCH --account=ornl-users
#SBATCH --gres=gpu:1

srun /scratch/gqe/install/add_rng_advance_kernel-b04f067/release-orange-trackslot-ranlux/bin/celer-optical run-gpu.1.json
