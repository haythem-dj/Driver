import matplotlib.pyplot as plt
import numpy as np
import math


def subplot_shape(l):
    if l <= 0:
        raise ValueError("l must be a positive integer")

    rows = math.ceil(math.sqrt(l))
    cols = math.ceil(l / rows)

    return rows, cols


def read_file(file):
    with open(file) as f:
        variables = {}
        num_points = 0

        for line in f:
            if "No. Points" in line:
                num_points = int(line.split()[-1])
            elif line.startswith("Variables"):
                break

        for line in f:
            if "Values" in line:
                break

            vs = line.strip().split()
            variables[vs[1]] = {"description": vs[2], "data": np.zeros(num_points)}

        keys = list(variables.keys())

        col = 0
        row = -1
        for line in f:
            line = line.strip()
            if line == "":
                continue

            v = line.split()

            if len(v) == 2:
                row += 1
                col = 0

            try:
                key = keys[col]
                variables[key]["data"][row] = float(v[-1])
            except ValueError:
                break
            col += 1

    return variables


data_file = "test.data"
variables = read_file(data_file)
keys = list(variables.keys())
rows, cols = subplot_shape(len(keys) - 1)
fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
axes = np.array(axes).flatten()

if "time" not in variables:
    raise ValueError("no 'time' variable found in data file")

time = variables["time"]["data"]

for i in range(1, len(keys)):
    ax = axes[i - 1]
    key = keys[i]
    ax.plot(time, variables[key]["data"])
    ax.grid()
    ax.set_xlabel("time")
    ax.set_ylabel(key)

plt.tight_layout()

plt.show()
