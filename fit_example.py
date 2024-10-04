import fit_black_box as bb

def linear(t, m, b):
    return m*t + b

def expon(t, a, b):
    return a*bb.np.exp(-t/b)

def quadratic(t, a, b, c):
    return a*t**2 + b*t + c

# init_guess = (-0.5, 0, +0.5)
# font_size = 20
# xlabel = "Time (s)"
# ylabel = "Height (m)"

# bb.plot_fit(quadratic, x, y, xerr, yerr, init_guess=init_guess, font_size=font_size, xlabel=xlabel, ylabel=ylabel)

# filename = "FINALDATA.txt"
# x, y, xerr, yerr = bb.load_data(filename)
# bb.plot_fit(quadratic, x, y, xerr, yerr)

filename = "FINALDATA.txt"
x, y, xerr, yerr = bb.load_data(filename)
bb.plot_fit(quadratic, x, y, xerr, yerr)

# filename = "FINALDATA.txt"
# x, y, xerr, yerr = bb.load_data(filename)
# bb.plot_fit(logar, x, y, xerr, yerr)