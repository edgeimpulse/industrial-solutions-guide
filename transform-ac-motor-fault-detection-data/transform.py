#!/usr/bin/env python
import numpy as np
import math, os, sys, argparse, json, hmac, hashlib, time
import pandas as pd

# these are the three arguments that we get in
parser = argparse.ArgumentParser(description='Organization transformation block')
parser.add_argument('--in-file', type=str, required=True)
parser.add_argument('--out-directory', type=str, required=True)

args, unknown = parser.parse_known_args()

json_data = {
    "protected": {
        "ver": "v1",
        "alg": "none",
    },
    "signature": "0000000000000000000000000000000000000000000000000000000000000000",
    "payload": {
        "device_name": "Dataset for Sensorless Drive Diagnosis",
        "device_type": "Dataset",
        "interval_ms": 0.01,
        "sensors": [
            { "name": "axis0", "units": "A" },
            { "name": "axis1", "units": "A" },
            { "name": "axis2", "units": "A" }
        ],
        "values": []
    }
}

# verify that the input file exists and create the output directory if needed
if not os.path.exists(args.in_file):
    print('--in-file argument', args.in_file, 'does not exist', flush=True)
    exit(1)

if not os.path.exists(args.out_directory):
    os.makedirs(args.out_directory)

# load and parse the input file
print('Loading input file', args.in_file, flush=True)
data_frame = pd.read_csv(args.in_file, delim_whitespace=True)

json_data['payload']['values'] = data_frame.values.tolist()

# and store as new file in the output directory
# new file name is classN.parameterN.json
out_file = os.path.join(args.out_directory, os.path.splitext(os.path.basename(args.in_file))[0].replace('_', '.') + '.json')

with open(out_file, 'w+') as f:
    json.dump(json_data, f)

print('Written .json file', out_file, flush=True)
