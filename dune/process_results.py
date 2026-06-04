#!/usr/bin/env python3

import json
import csv

# Define number of runs
num_runs = 10

# Prepare data for writing CSV file
fieldnames = ['run', 'absorption', 'along-step', 'boundary-init', 'boundary-post', 'discrete-select', 
              'locate-vacancies', 'pre-step', 'primary-generate', 'rayleigh', 'surface-physics', 
              'tracking-cut', "setup", "total"]
kernels = ["primary-generate", "pre-step", "rayleigh", "rng-reseed"]
kernel_fieldnames = ['kernel', 'num_regs', 'occupancy', 'local_mem']
fielddata = list()
kerneldata = list()

# Extract the timing and kernel data from all of the runs
core_rng = None
reseed = None
for i in range(num_runs):
    
    # Open the JSON file for run i
    input_filename = "run_{}/out.{}.json".format(i, i)
    with open(input_filename, "r", encoding="utf-8") as input:

        # Read and parse the JSON file
        json_input = json.load(input)

        # Print what kind of run this is
        if core_rng is None:
            core_rng = json_input['system']['build']['config']['core_rng']
            print("These runs used the {} RNG".format(core_rng))
        else:
            assert(json_input['system']['build']['config']['core_rng'] == core_rng)
        if reseed is None:
            reseed = json_input['system']['build']['config']['reseed']
            print("These runs used the {} RNG".format(reseed))
        else:
            assert(json_input['system']['build']['config']['reseed'])

        # Load the kernel data 
        print(json_input['system']['kernels'][0].keys())
        kern_data = list()
        for k in json_input['system']['kernels']:
            if k['name'] in kernels:
                this_kern = dict()
                this_kern['kernel'] = k['name']
                for n in kernel_fieldnames[1:]:
                    this_kern[n] = k[n]
                kern_data.append(this_kern)
        kerneldata.append(kern_data)

        # Load the timings into a dictionary
        data = dict();
        data["run"] = i
            
        # Get the action timings
        for fn in fieldnames[1:-2]:
            data[fn] = float(json_input['result']['time']['actions'][fn])
        
        # Get the summary timings
        for fn in fieldnames[-2:]:
            data[fn] = float(json_input['result']['time'][fn])

            
        # Append to the CSV field
        fielddata.append(data)

# Write the CSV file for the detailed timing information for all of the runs
detailed_timings_filename = "detailed_timings.csv"
with open(detailed_timings_filename, "a", newline="\n", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fielddata)
print("Wrote detailed timings to {}".format(detailed_timings_filename))

# Write the CSV field for the detailed kernel information for all of the runs
#print(kerneldata)
detailed_kernel_filename = "detailed_kernel_info.csv"
with open(detailed_kernel_filename, "w", newline="\n", encoding="utf-8") as output:
    for i in range(num_runs):
        output.write("Run {}\n".format(i))
        writer = csv.DictWriter(output, fieldnames=kernel_fieldnames)
        writer.writeheader()
        writer.writerows(kerneldata[i])
print("Wrote detailed kernel info to {}".format(detailed_kernel_filename))

# Process the field data to get timing averages over all of the runs
avg_data = dict()
for fn in fieldnames:
    
    # Construct a list of field fn over all runs
    list_data = [fielddata[i][fn] for i in range(num_runs)]
    
    # Compute the average and store in the dictionary
    avg_data[fn] = sum(list_data) / num_runs

# Write the CSV file for the average timing information
average_timings_filename = "average_timings.csv"
with open("average_timings.csv", "w", newline="\n", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([avg_data])
print("Wrote average timings to {}".format(average_timings_filename))

# Process the kernel data to get averages over all of the runs
#avg_kernel_data = dict()
#for kn in kernel_fieldnames:

    # Construct a list of field data over all runs
 #   list_data = [kerneldata[i][]
