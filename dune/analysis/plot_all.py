import json
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Times font everywhere
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"]
mpl.rcParams["mathtext.fontset"] = "stix"

class JsonReader(object):

    def __init__(self, json_file):
        with open(json_file, "rb") as f:
            self._data = json.load(f)

    def get(self, json_path):
        keys = str(json_path).split("/")
        cur = self._data
        for k in keys:
            cur = cur[k]

        return float(cur)

def plot_track_slots(prefix):
    plt.gca().clear()

    trials = [2**x for x in range(15, 27)]
    
    along_step = []
    total = []
    
    for trial in trials:
        reader = JsonReader("{}/track_slots/stdout_{}.json".format(prefix, trial))
        along_step.append(reader.get("result/time/actions/along-step"))
        total.append(reader.get("result/time/total"))
    
    print(trials)
    print(along_step)
    print(total)
    print()
    
    plt.plot(trials, total, label="total")
    plt.plot(trials, along_step, label="along-step")
    plt.ylabel("run time (s)")
    plt.xlabel("number of track slots")
    plt.xscale("log", base=2)
    #plt.ylim([0, 120])
    legend = plt.legend(loc="best", frameon=True, fancybox=False,
                        framealpha=1, edgecolor="inherit")
    legend.get_frame().set_linewidth(mpl.rcParams["axes.linewidth"])
    
    plt.savefig("{}_plots/track_slots.pdf".format(prefix, bbox_inches="tight"))


def plot_max_leaf_size(prefix):
    plt.gca().clear()

    trials = [int(x) for x in np.logspace(0, 4.5, 10)]
    
    along_step = []
    total = []
    
    for trial in trials:
        reader = JsonReader("{}/max_leaf_size/stdout_{}.json".format(prefix, trial))
        along_step.append(reader.get("result/time/actions/along-step"))
        total.append(reader.get("result/time/total"))
    
    print(trials)
    print(along_step)
    print(total)
    print()
    
    plt.plot(trials, total, label="total")
    plt.plot(trials, along_step, label="along-step")
    plt.ylabel("run time (s)")
    plt.xlabel("maximum leaf size")
    plt.xscale("log", base=10)
    #plt.ylim([0, 120])
    plt.title("num_track_slots = $2^{18}$")

    legend = plt.legend(loc="best", frameon=True, fancybox=False,
                        framealpha=1, edgecolor="inherit")
    legend.get_frame().set_linewidth(mpl.rcParams["axes.linewidth"])
    
    plt.savefig("{}_plots/max_leaf_size.pdf".format(prefix), bbox_inches="tight")


def plot_depth_limit(prefix):
    plt.gca().clear()

    trials = [int(x) for x in range(1, 11)]
    
    along_step = []
    total = []
    
    for trial in trials:
        reader = JsonReader("{}/depth_limit/stdout_{}.json".format(prefix, trial))
        along_step.append(reader.get("result/time/actions/along-step"))
        total.append(reader.get("result/time/total"))
    
    print(trials)
    print(along_step)
    print(total)
    print()
    
    plt.plot(trials, total, label="total")
    plt.plot(trials, along_step, label="along-step")
    plt.ylabel("run time (s)")
    plt.xlabel("depth limit")
    #plt.ylim([0, 120])
    plt.title("num_track_slots = $2^{18}$, max_leaf_size = 100, depth w/o limit = 10")

    legend = plt.legend(loc="best", frameon=True, fancybox=False,
                        framealpha=1, edgecolor="inherit")
    legend.get_frame().set_linewidth(mpl.rcParams["axes.linewidth"])
    
    plt.savefig("{}_plots/depth_limit.pdf".format(hudson), bbox_inches="tight")

def plot_part_cands(prefix):
    plt.gca().clear()

    trials = [3**x for x in range(0, 8)]
    
    along_step = []
    total = []
    
    for trial in trials:
        reader = JsonReader("{}/part_cands/stdout_{}.json".format(prefix, trial))
        along_step.append(reader.get("result/time/actions/along-step"))
        total.append(reader.get("result/time/total"))
    
    print(trials)
    print(along_step)
    print(total)
    print()
    
    plt.plot(trials, total, label="total")
    plt.plot(trials, along_step, label="along-step")
    plt.ylabel("run time (s)")
    plt.xlabel("number of partition candidates")
    plt.xscale("log", base=3)
    #plt.ylim([0, 120])
    legend = plt.legend(loc="best", frameon=True, fancybox=False,
                        framealpha=1, edgecolor="inherit")
    legend.get_frame().set_linewidth(mpl.rcParams["axes.linewidth"])
    
    plt.savefig("{}_plots/part_cands.pdf".format(prefix, bbox_inches="tight"))


prefix = sys.argv[1]
plot_track_slots(prefix)
plot_max_leaf_size(prefix)
#plot_depth_limit(prefix)
#plot_part_cands(prefix)
