#!/bin/bash
#SBATCH --job-name=dune_cpu_track_ranlux_0
#SBATCH --chdir=/home/gqe/Codes/celeritas/analysis/celer_analysis/dune/add_rng_advance_kernel-b04f067/cpu_track_ranlux/run_0
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --partition=hudson
#SBATCH --account=ornl-users
export CELER_DISABLE_DEVICE=1

srun /scratch/gqe/install/add_rng_advance_kernel-b04f067/release-orange-track-ranlux/bin/celer-optical run-cpu.0.json
