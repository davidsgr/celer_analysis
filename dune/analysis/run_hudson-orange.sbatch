#!/bin/bash
#SBATCH -p nvidia
#SBATCH -w hudson
#SBATCH -t 04:00:00
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH -J celer-sim
#SBATCH -o slurm_out
#SBATCH -e slurm_err

set -euo pipefail

load_system_env() {
  CELER_SOURCE_DIR="/home/veb/opt/celeritas/celeritas"
  if [ -d "${CELER_SOURCE_DIR}" ]; then
    . "${CELER_SOURCE_DIR}/scripts/env/$1.sh"
  fi
}

export SYSTEM_NAME=hudson
export G4_GEO_OPTIMIZE=0
export CMAKE_PREFIX_PATH=/scratch/veb/build/celeritas-release-orange/
export PATH=$PATH:/scratch/veb/build/celeritas-release-orange/bin/

source /auto/projects/celeritas/spack/share/spack/setup-env.sh
load_system_env hudson

python sweep_all.py hudson-orange
