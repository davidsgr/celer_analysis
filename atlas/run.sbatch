#!/bin/bash
#SBATCH -p nvidia
#SBATCH -w hudson
#SBATCH -t 01:00:00
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH -J celer-sim
#SBATCH -o stdout.json
#SBATCH -e stderr

set -euo pipefail

load_system_env() {
  CELER_SOURCE_DIR="/home/veb/opt/celeritas/celeritas"
  if [ -d "${CELER_SOURCE_DIR}" ]; then
    . "${CELER_SOURCE_DIR}/scripts/env/$1.sh"
  fi
}

export SYSTEM_NAME=hudson
#export CELER_LOG=debug
#export CELER_LOG_LOCAL=debug 
export G4_GEO_OPTIMIZE=0
export CMAKE_PREFIX_PATH=/scratch/veb/build/celeritas-reldeb-orange/
export PATH=$PATH:/scratch/veb/build/celeritas-reldeb-orange/bin/

source /auto/projects/celeritas/spack/share/spack/setup-env.sh
load_system_env hudson

# Run
# celer-sim run.json
nsys profile -f true --trace=cuda,nvtx --sample=none -o celer-sim celer-sim run.json

