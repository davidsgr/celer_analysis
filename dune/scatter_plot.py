#!/usr/bin/env python3
"""
Read x,y coordinates from a text file and create a scatter plot.

Expected input format: one point per line, for example:

    1.0, 2.5
    3.2, 4.1
    5.0, 1.7

Whitespace-separated values also work:

    1.0 2.5
    3.2 4.1
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(
        description="Create a scatter plot from a file of x,y coordinates."
    )
    parser.add_argument("input_file", help="Text file containing x,y coordinates")
    parser.add_argument(
        "-o", "--output",
        help="Optional output image filename, e.g. plot.png"
    )
    args = parser.parse_args()

    # delimiter=None accepts whitespace-separated data.
    # delimiter="," accepts comma-separated data.
    #
    # Use np.genfromtxt because it handles blank lines and comments well.
    try:
        data = np.genfromtxt(
            args.input_file,
            delimiter=",",
            comments="#",
            dtype=float
        )

        # If comma parsing did not produce two columns, try whitespace parsing.
        if data.ndim == 1 or (data.ndim == 2 and data.shape[1] != 2):
            data = np.genfromtxt(
                args.input_file,
                delimiter=None,
                comments="#",
                dtype=float
            )

    except OSError as e:
        raise SystemExit(f"Could not read '{args.input_file}': {e}")

    # Ensure one row such as "1.0, 2.0" is treated as shape (1, 2).
    data = np.atleast_2d(data)

    if data.shape[1] != 2:
        raise SystemExit(
            "Expected exactly two columns per line: x,y or x y."
        )

    x = data[:, 0]
    y = data[:, 1]


    # Write scatter plot
    #plt.figure(figsize=(7, 5))
    #plt.scatter(x[:5000], y[:5000], s=25)
    #plt.xlabel("cos(theta)")
    #plt.ylabel("phi")
    #plt.title("Scatter Plot")
    #plt.grid(True, alpha=0.3)
    #plt.tight_layout()

    # Write histogram plot
    bins = 50
    counts, bin_edges, _ = plt.hist(
        x,
        bins=bins,
        edgecolor="black",
        alpha=0.75,
    )

    plt.xlabel("Cos(Theta)")
    plt.ylabel("Count")
    plt.title("Histogram of cos(theta) Values")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    if args.output:
        plt.savefig(args.output, dpi=200)
        print(f"Saved plot to: {args.output}")
    else:
        plt.show()



if __name__ == "__main__":
    main()
