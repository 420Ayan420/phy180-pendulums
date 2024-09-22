# -*- coding: utf-8 -*-
"""
This script generates a scatter plot from a given data file.
The first line of the file is ignored (assumed to be headers).
The data file should contain multiple columns: x_data y1 y2 y3.
"""

import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt

def load_data(filename):
    """Load data from a file, ignoring the first line."""
    data = loadtxt(filename, skiprows=1)
    xdata = data[:, 0]  # First column as x values
    ydata = data[:, 1:]  # Subsequent columns as y values
    return xdata, ydata

def create_scatter_plot(xdata, ydata, font_size=14, xlabel="Initial Angle (rad)", ylabel="Pendulum Period (s)", title="Scatter Plot for Initial Angle versus Pendulum Period"):
    """Create a scatter plot of the provided data."""
    plt.rcParams.update({'font.size': font_size})
    plt.figure(figsize=(10, 6))

    # Plot each y series with different colors
    for i in range(ydata.shape[1]):
        plt.scatter(xdata, ydata[:, i], label=f'Y{i + 1}', marker='o')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    plt.savefig("scatter_plot.png")
    print("Scatter plot saved as scatter_plot.png")

if __name__ == "__main__":
    filename = "scatter1L.txt"  # Make sure this file exists in the same directory
    x, y = load_data(filename)

    create_scatter_plot(x, y)
