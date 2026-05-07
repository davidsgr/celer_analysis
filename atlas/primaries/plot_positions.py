#!/usr/bin/env python3
"""
Read a CSV-like file with lines: x,y,z (no header) and plot the points in 3D.

Usage:
  python plot_points3d.py positions.csv
"""

import sys
import numpy as np
import matplotlib.pyplot as plt


def load_xyz(path: str) -> np.ndarray:
    # Robust to whitespace; expects 3 columns separated by commas
    data = np.loadtxt(path, delimiter=",", dtype=float)
    if data.ndim == 1:
        # Single line file -> shape (3,)
        if data.size != 3:
            raise ValueError(f"Expected 3 values per line, got {data.size}")
        data = data.reshape(1, 3)
    if data.shape[1] != 3:
        raise ValueError(f"Expected 3 columns (x,y,z); got shape {data.shape}")
    return data


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python plot_points3d.py <positions.csv>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    xyz = load_xyz(path)
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # For large point clouds, use a small marker size
    ax.scatter(x, y, z, s=1)

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("z (cm)")

    # Optional: make axes roughly equal scale (matplotlib doesn't do this by default)
    mins = xyz.min(axis=0)
    maxs = xyz.max(axis=0)
    centers = (mins + maxs) / 2.0
    spans = (maxs - mins)
    radius = 0.5 * spans.max()
    ax.set_xlim(centers[0] - radius, centers[0] + radius)
    ax.set_ylim(centers[1] - radius, centers[1] + radius)
    ax.set_zlim(centers[2] - radius, centers[2] + radius)

    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

