#!/usr/bin/env python3

import json
import csv

# Define number of runs
num_runs = 10

# Prepare data for writing CSV file
fieldnames = ["run", "along-step-neutral", "along-step-uniform-msc", "initialize-tracks", "setup", "total"]
fielddata = list()
    
# Extract the timing data from all of the runs
for i in range(num_runs):
    
    # Open the JSON file for run i
    input_filename = "run_{}/out.{}.json".format(i, i)
    with open(input_filename, "r", encoding="utf-8") as input:

        # Read and parse the JSON file
        json_input = json.load(input)

        # Load the timings into a dictionary
        data = dict();
        data["run"] = i
            
        # Get the action timings
        for fn in fieldnames[1:-2]:
            #print(json_input['result']['runner']['time']['actions'])
            data[fn] = float(json_input['result']['runner']['time']['actions'][fn])
        
        # Get the summary timings
        for fn in fieldnames[-2:]:
            data[fn] = float(json_input['result']['runner']['time'][fn])
            
        # Append to the CSV field
        fielddata.append(data)

# Write the CSV file for the detailed timing information for all of the runs
detailed_timings_filename = "detailed_timings.csv"
with open(detailed_timings_filename, "w", newline="\n", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fielddata)
print("Wrote detailed timings to {}".format(detailed_timings_filename))

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

