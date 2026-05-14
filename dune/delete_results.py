#!/usr/bin/env python3
from pathlib import Path
import shutil

# Delete all of the results
output_prefix = "trackslot_xorwow"
num_runs = 10
for i in range(num_runs):
    p = Path(output_prefix + "/run_{}".format(i))
    if p.exists():
        shutil.rmtree(p)
