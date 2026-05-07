import os
import numpy as np
import subprocess
import shutil
import sys
import json

def write_temp_with_track_slots(num_track_slots):
    with open("run.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        data["problem"]["capacity"]["tracks"] = num_track_slots

    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

###############################################################################

def sweep_track_slots(prefix):


    trials = [2**x for x in range(15, 30)]
    
    outdir = "{}/track_slots".format(prefix)
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    
    for trial in trials:
    
        write_temp_with_track_slots(trial)
    
        with open(f"{outdir}/stdout_{trial}.json", "w") as f_out, open(os.devnull, "w") as f_err:
            subprocess.run(["celer-optical", "temp.json"], stdout=f_out, stderr=f_err, check=False)
    
        os.remove("temp.json")

###############################################################################

def sweep_max_leaf_size(prefix, track_slots):

    trials = [int(x) for x in np.logspace(0, 4.5, 10)]
    
    outdir = "{}/max_leaf_size".format(prefix)
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    
    for trial in trials:

        write_temp_with_track_slots(track_slots)

        env = os.environ.copy()
        env["ORANGE_BIH_MAX_LEAF_SIZE"] = str(trial)
    
        with open(f"{outdir}/stdout_{trial}.json", "w") as f_out, open(os.devnull, "w") as f_err:
            subprocess.run(["celer-optical", "temp.json"], env=env, stdout=f_out, stderr=f_err, check=False)

        os.remove("temp.json")

################################################################################
#
#def sweep_depth_limit(prefix):
#    trials = range(1, 11)
#    
#    outdir = "{}/depth_limit".format(prefix)
#    shutil.rmtree(outdir, ignore_errors=True)
#    os.makedirs(outdir)
#    
#    for trial in trials:
#        env = os.environ.copy()
#        env["ORANGE_BIH_MAX_LEAF_SIZE"] = "100"
#        env["ORANGE_BIH_DEPTH_LIMIT"] = str(trial)
#    
#        with open(f"{outdir}/stdout_{trial}.json", "w") as f_out, open(os.devnull, "w") as f_err:
#            subprocess.run(["celer-optical", "run.json"], env=env, stdout=f_out, stderr=f_err, check=False)
#
################################################################################
#
#def sweep_part_cands(prefix):
#    trials = [3**x for x in range(0, 8)]
#    
#    outdir = "{}/part_cands".format(prefix)
#    shutil.rmtree(outdir, ignore_errors=True)
#    os.makedirs(outdir)
#    
#    for trial in trials:
#        env = os.environ.copy()
#        env["ORANGE_BIH_MAX_LEAF_SIZE"] = "100"
#        env["ORANGE_BIH_PART_CANDS"] = str(trial)
#    
#        with open(f"{outdir}/stdout_{trial}.json", "w") as f_out, open(os.devnull, "w") as f_err:
#            subprocess.run(["celer-optical", "run.json"], env=env, stdout=f_out, stderr=f_err, check=False)


###############################################################################
# DRIVER
###############################################################################s

prefix = sys.argv[1]

hudson_track_slots = 67108864


#sweep_track_slots(prefix)
sweep_max_leaf_size(prefix, hudson_track_slots)

#sweep_depth_limit(prefix)
#sweep_part_cands(prefix)
