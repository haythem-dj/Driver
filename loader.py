import numpy as np
import argparse
import sys
import os
import json


def load_data(file_name):
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' was not found.")
        sys.exit(1)

    with open(file_name) as f:
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

            parts = line.split()

            if len(parts) == 2:
                row += 1
                col = 0

            try:
                key = keys[col]
                variables[key]["data"][row] = float(parts[-1])
            except ValueError:
                break
            col += 1

    return variables


def main():
    parser = argparse.ArgumentParser(
        description="Parse ngspice data (ascii) and export it as JSON."
    )

    parser.add_argument(
        "-i", "--input", required=True, help="The input ngspice data file."
    )

    parser.add_argument("-o", "--output", help="The output JSON file.")

    args = parser.parse_args()
    output_file = (
        args.output if args.output else f"{os.path.splitext(args.input)[0]}.json"
    )

    variables = load_data(args.input)

    if "time" not in variables:
        raise ValueError("no 'time' variable found in data file")

    output = {
        key: {"description": val["description"], "data": val["data"].tolist()}
        for key, val in variables.items()
    }

    with open(output_file, "w") as file:
        json.dump(output, file, indent=4)

    print(f"{output_file} is generated.")


if __name__ == "__main__":
    main()
