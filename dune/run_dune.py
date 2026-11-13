#!/usr/bin/env python3

import json
from pathlib import Path
import os
import subprocess
import sys

# Slurm settings: override via environment variables
SLURM_PARTITION = "hudson"
SLURM_ACCOUNT = "ornl-users"
SLURM_GPU_GRES = "gpu:1"
SLURM_CPUS = "1"
SLURM_TIME_GPU = "00:30:00"
SLURM_TIME_CPU = "4:00:00"

# Write batch scripts but do not call sbatch
DRY_RUN = "--dry-run" in sys.argv

seeds = [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 1234]

base_install_path = "/scratch/gqe/install/add_rng_advance_kernel-b04f067/"

def run_problem(mode, reseed, rng):
    assert mode == "cpu" or mode == "gpu"
    assert reseed == "track" or reseed == "trackslot"
    assert rng == "ranlux" or rng == "xorwow"

    # If we are running GPU, we run 10 runs and average their results
    # If we are running CPU, DUNE is too expensive to run 10 runs, so we'll just run 1
    num_runs = 10
    if (mode == "cpu"):
        num_runs = 1
    print(">>> Running Celeritas on the {} with {} reseeding and the {} RNG".format(mode.upper(), reseed, rng))

    # Create input files
    base_file = "run-{}.base.json".format(mode)
    output_prefix = "{}_{}_{}".format(mode, reseed, rng)
    with open(base_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
        for i in range(num_runs):
            # Change the output file name to out-[mode].i.json
            data['problem']['output_file'] = "out-{}.{}.json".format(mode, i)
        
            # Change the seed
            data['problem']['seed'] = seeds[i]

            # Create a directory to hold the run
            Path(output_prefix).mkdir(exist_ok=True)
            Path(output_prefix + "/run_{}".format(i)).mkdir(exist_ok=True)

            # Write to run.i.json
            output_filename = base_file.replace("base", str(i))
            with open(output_prefix + "/run_{}/".format(i) + output_filename, "w", encoding="utf-8") as of:
                json.dump(data, of)

    # Submit one Slurm job per run
    celer_path = base_install_path + "release-orange-{}-{}/bin/".format(reseed, rng)
    #celer_path = base_install_path + "/bin/".format(reseed, rng)
    job_ids = []
    for i in range(num_runs):
        run_dir = Path(output_prefix) / "run_{}".format(i)
        input_file = "run-{}.{}.json".format(mode, i)
        job_name = "dune_{}_{}_{}_{}".format(mode, reseed, rng, i)
        job_id = submit_job(job_name, run_dir.resolve(), celer_path + "celer-optical", input_file, mode)
        print("## Submitted Celeritas run {}/{} as Slurm job {}".format(i + 1, num_runs, job_id))
        job_ids.append(job_id)
    return job_ids


def submit_job(job_name, run_dir, executable, input_file, mode):
    """Write a batch script in run_dir and submit it with sbatch.

    Returns the Slurm job ID as a string.
    """
    lines = [
        "#!/bin/bash",
        "#SBATCH --job-name={}".format(job_name),
        "#SBATCH --chdir={}".format(run_dir),
        "#SBATCH --output=slurm-%j.out",
        "#SBATCH --error=slurm-%j.err",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        "#SBATCH --cpus-per-task={}".format(SLURM_CPUS),
        "#SBATCH --time={}".format(SLURM_TIME_GPU if mode == "gpu" else SLURM_TIME_CPU),
    ]
    if SLURM_PARTITION:
        lines.append("#SBATCH --partition={}".format(SLURM_PARTITION))
    if SLURM_ACCOUNT:
        lines.append("#SBATCH --account={}".format(SLURM_ACCOUNT))
    if mode == "gpu":
        lines.append("#SBATCH --gres={}".format(SLURM_GPU_GRES))
    else:
        # Make sure CPU runs never see a device
        lines.append("export CELER_DISABLE_DEVICE=1")
    lines += ["", "srun {} {}".format(executable, input_file), ""]

    script = run_dir / "submit.sbatch"
    script.write_text("\n".join(lines), encoding="utf-8")

    if DRY_RUN:
        print("## [dry run] would submit {}".format(script))
        return "DRYRUN"
    result = subprocess.run(["sbatch", "--parsable", str(script)],
                            check=True, capture_output=True, text=True)
    # --parsable prints "jobid" or "jobid;cluster"
    return result.stdout.strip().split(";")[0]


if __name__ == "__main__":
    all_jobs = []
    for m in ["cpu", "gpu"]:
        for s in ["trackslot", "track"]:
            for r in ["ranlux", "xorwow"]:
                all_jobs += run_problem(m, s, r)
    print(">>> Submitted {} jobs. Monitor with: squeue -u $USER".format(len(all_jobs)))

