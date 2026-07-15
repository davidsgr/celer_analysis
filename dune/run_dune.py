#!/usr/bin/env python3

import json
from pathlib import Path
import os
import subprocess

seeds = [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 1234]

base_install_path = "/scratch/gqe/install/develop-dc56207d6ef907c02c0523aaf3dede99086c627c/"

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

    # Run celeritas
    for i in range(num_runs):

        # Enter run directory
        os.chdir(output_prefix + "/run_" + str(i))

        # Run celeritas
        celer_path = base_install_path + "release-orange-{}-{}/bin/".format(reseed, rng)
        #celer_path = base_install_path + "/bin/".format(reseed, rng)
        print("## Running Celeritas {}/{}.".format(i + 1, num_runs))
        subprocess.run([celer_path + "celer-optical", "run-{}.{}.json".format(mode, i)], check=True)

        # Exit run directory
        os.chdir("../..")


if __name__ == "__main__":
    for m in ["cpu", "gpu"]:
        for s in ["trackslot", "track"]:
            for r in ["xorwow", "ranlux"]:
                run_problem(m, s, r)

