import matplotlib.pyplot as plt
import numpy as np
import argparse
import math
import json
import sys
import os


def subplot_shape(l):
    if l <= 0:
        raise ValueError("l must be a positive integer")

    rows = math.ceil(math.sqrt(l))
    cols = math.ceil(l / rows)

    return rows, cols

def main():
    parser = argparse.ArgumentParser(
        description="Read ngspice data as JSON and plot them as a png."
    )

    parser.add_argument(
        "-i", "--input", required=True,
        help="ngspice data JSON file."
    )

    parser.add_argument(
        "-o", "--output", required=True,
        help="PNG file name."
    )

    parser.add_argument(
        "-t", "--title",
        help="A title for the plot.",
        default="Data Visualising"
    )

    parser.add_argument(
        "-inc", "--include",
        nargs="+",
        help="The names of the variables to export."
    )

    args = parser.parse_args()

    with open(args.input, "r") as f:
        variables = json.load(f)

    if "time" not in variables:
        raise ValueError("no 'time' variable found in data file")
    time = variables["time"]["data"]

    if args.include:
        keys_to_plot = [k for k in args.include if k in variables and k != "time"]
        if not keys_to_plot:
            print(f"Error: None of the requested variables '{args.include}' found in data.")
            sys.exit(1)

    else:
        keys_to_plot = [k for k in variables if k != "time"]


    rows, cols = subplot_shape(len(keys_to_plot))
    _, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
    axes = np.array(axes).flatten()

    for i, key in enumerate(keys_to_plot):
        ax = axes[i]
        ax.plot(time, variables[key]["data"])
        ax.set_xlabel("time")
        ax.set_ylabel(key)
        ax.grid(True)

    plt.suptitle(args.title)
    plt.tight_layout()

    root, ext = os.path.splitext(args.output)
    output = f"{root}.png"

    plt.savefig(output, bbox_inches="tight")

    print(f"Plot save as {output}")

if __name__ == "__main__":
    main()
