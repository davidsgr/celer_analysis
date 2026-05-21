#!/usr/bin/env python3

import json
from pathlib import Path
import os
import subprocess

base_file = "run.base.json"
num_runs = 10
seeds = [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 1234]
output_prefix = "trackslot_xorwow"

# Create input files
with open("run.base.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
    for i in range(num_runs):
        # Change the output file name to run.i.json
        data['output_file'] = "out.{}.json".format(i)
        
        # Change the seed
        data['seed'] = seeds[i]

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

    # Set the output path
    output_file = "out.{}.json".format(i)

    # Run celeritas
    celer_path = "/scratch/gqe/install/celeritas-release-orange-track-ranlux/bin/"
    cmd = [celer_path + "celer-sim", "run.{}.json".format(i)]
    with open(output_file, "w", encoding="utf-8") as output:
       print("Running Celeritas {}/{}.".format(i+1, num_runs))
       subprocess.run(cmd, check=True, stdout=output)

    # Exit run directory
    os.chdir("../..")

