# -*- coding: utf-8 -*-
"""
This program takes a data file with 6 columns: 
x_max_time, x_max_displacement, x_min_time, x_min_displacement, x_max_error_percentage, x_min_error_percentage.
It fits an exponential or other functions to the data using a dropdown menu to select the curve type.
It also plots the data, residuals, and the best fit line for both max and min displacements.

Note: The data file should have space or tab-separated columns.
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from matplotlib.widgets import RadioButtons
from pylab import loadtxt

def load_data(filename):
    """
    Function to load data from a file.
    The file should have 6 columns: x_max_time, x_max_displacement, x_min_time, 
    x_min_displacement, x_max_error%, x_min_error%.
    The first line is skipped (assumed to be headers).
    """
    data = loadtxt(filename, usecols=(0,1,2,3,4,5), skiprows=1, unpack=True)
    return data

def plot_fit(my_func, xdata, ydata, yerror, init_guess, xlabel="Time", ylabel="Displacement", title="Displacement vs Time"):
    """
    Function to fit the curve and plot the data with error bars.
    Also plots the residuals below the main graph.
    """
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['figure.figsize'] = 10, 9

    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess, absolute_sigma=True)
    puncert = np.sqrt(np.diagonal(pcov))

    print("Best fit parameters, with uncertainties:")
    for i in range(len(popt)):
        print(f"{popt[i]:.4f} +/- {puncert[i]:.4f}")

    # Creating the smooth curve for best fit
    start = min(xdata)
    stop = max(xdata)
    xs = np.linspace(start, stop, 1000)
    curve = my_func(xs, *popt)

    # Plotting the data and the fit
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
    
    # Plot positive and negative data points separately
    positive_indices = ydata >= 0
    negative_indices = ydata < 0

    ax1.errorbar(xdata[positive_indices], ydata[positive_indices], yerr=yerror[positive_indices], fmt=".", label="Positive Data", color="black")
    ax1.errorbar(xdata[negative_indices], ydata[negative_indices], yerr=yerror[negative_indices], fmt=".", label="Negative Data", color="blue")
    
    ax1.plot(xs, curve, label="Best Fit", color="red")
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    ax1.legend()

    # Residuals
    residuals = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residuals, yerr=yerror, fmt=".", color="black")
    ax2.axhline(y=0, color="red")
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel("Residuals")

    fig.tight_layout()
    plt.show()
    return popt

def exponential_func(t, a, b, c):
    """Exponential function: y = a * exp(b * t) + c"""
    return a * np.exp(b * t) + c

def linear_func(t, m, b):
    """Linear function: y = m * t + b"""
    return m * t + b

def quadratic_func(t, a, b, c):
    """Quadratic function: y = a * t^2 + b * t + c"""
    return a * t**2 + b * t + c

def plot_with_dropdown(max_time, max_data, min_time, min_data, max_err, min_err):
    """
    Plotting with a dropdown menu to switch between curve types.
    Fits both max and min data points.
    """

    # Default initial guess
    init_guess_max = (1, -0.1, 1)
    init_guess_min = (1, -0.1, 1)

    # Default function
    fit_func = exponential_func

    # Plot with default function
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3)
    popt_max = plot_fit(fit_func, max_time, max_data, max_err, init_guess_max, title="Max Displacement")
    popt_min = plot_fit(fit_func, min_time, min_data, min_err, init_guess_min, title="Min Displacement")

    # Adding radio buttons to switch between functions
    ax_radio = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor="lightgoldenrodyellow")
    radio = RadioButtons(ax_radio, ('Exponential', 'Linear', 'Quadratic'))

    def update_curve(label):
        nonlocal fit_func
        if label == "Exponential":
            fit_func = exponential_func
        elif label == "Linear":
            fit_func = linear_func
        elif label == "Quadratic":
            fit_func = quadratic_func

        # Re-plot the curves based on selected function
        plot_fit(fit_func, max_time, max_data, max_err, init_guess_max, title="Max Displacement")
        plot_fit(fit_func, min_time, min_data, min_err, init_guess_min, title="Min Displacement")

    radio.on_clicked(update_curve)
    plt.show()

# Main code to load data, plot graphs, and allow for curve fitting
filename = "displacement_data.txt"
max_time, x_max, min_time, x_min, x_max_err_perc, x_min_err_perc = load_data(filename)

# Convert percentage errors to absolute errors
x_max_err = x_max * (x_max_err_perc / 100)
x_min_err = x_min * (x_min_err_perc / 100)

# Plot with dropdown to switch between curve types
plot_with_dropdown(max_time, x_max, min_time, x_min, x_max_err, x_min_err)
