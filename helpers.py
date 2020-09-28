#!/bin/env python3

import matplotlib.pyplot as plt
from os import system

# Make it look like LaTeX.
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
rc('text', usetex=True)

def store_state(list_electrons):
    # Gets list of Electron objects as input
    # and stores it as a file, because the calculation
    # to find equillibrium state is time-intensive.
    # Be sure to have correct directory structure already
    # set before running this!

    no_electrons = len(list_electrons)
    filename = './data/stored-states/{}-electrons/stored-state-{}.txt'.format(
        no_electrons, no_electrons)

    # Create directory if it does not yet exist.
    system('mkdir -p ./data/stored-states/{}-electrons/'.format(no_electrons))

    # Clear file if it exists and write new data to it.
    with open(filename, 'w') as dat:
        for electron in list_electrons:
            dat.write('{} {}\n'.format(electron.x, electron.y))


def plot_electrons(starting_state, equillibrium_state):
    # Plots starting and equillibrium states.
    plt.axis('equal')
    plt.plot([1, -1, -1, 1, 1], [1, 1, -1, -1, 1], color='black', alpha=0.7)
    plt.plot([i.x for i in starting_state],
            [i.y for i in starting_state], 'r.')
    plt.plot([i.x for i in equillibrium_state],
            [i.y for i in equillibrium_state], 'g.')
    plt.tick_params(which='both',       # Both major and minor ticks are affected.
                    bottom=False,       # Ticks along the bottom edge are off.
                    left=False,         # Ticks along the left edge are off.
                    labelbottom=False,  # Labels along the bottom edge are off.
                    labelleft=False)    # Labels along the left edge are off.
    plt.show()
