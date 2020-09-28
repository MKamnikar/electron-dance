#!/bin/env python3

from os import system
import numpy as np
import matplotlib.pyplot as plt
from random import random

# Make it look like LaTeX.
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
rc('text', usetex=True)


class Electron():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def put_electron_on_a_square(phi):
    # Accepts polar angle as input
    # and returns Electron class object
    # with proper x and y coordinates.

    # phi is periodical.
    phi = phi % (2*np.pi)

    if phi < np.pi/4:  # x = 1, y = ?
        return Electron(1, np.tan(phi))
    elif phi < 3/4*np.pi:  # x = ?, y = 1
        return Electron(-np.tan(phi - np.pi/2), 1)
    elif phi < 5/4*np.pi:  # x = -1, y = ?
        return Electron(-1, -np.tan(phi - np.pi))
    elif phi < 7/4*np.pi:  # x = ?, y = -1
        return Electron(np.tan(phi - 6/4*np.pi), -1)
    else:  # x = 1, y = ?
        return Electron(1, np.tan(phi))


def correct_position(index, list_electrons):
    # Accepts list of electrons as input and
    # index of a single electron.
    # Returns new Electron object with corrected
    # position which is closer to the equillibrium.

    def forces_on_electron(index, list_electrons):
        # Accepts list of electrons and the index of one
        # as input to calculate and return the component
        # of force of other electrons on the one, which is
        # parallel to the square conductor.
        single_electron = list_electrons[index]
        parallel_force_sum = 0
        if abs(single_electron.y) == 1:  # Force has to be parallel to x.
            for j in range(len(list_electrons)):
                if j != index:  # Don't calculate force on itself (NaN).
                    i = list_electrons[j]
                    parallel_force_sum += ((single_electron.x - i.x) / ((i.x - single_electron.x)**2 + (i.y - single_electron.y)**2)**1.5)
        else:  # Force has to be parallel to y axis.
            for j in range(len(list_electrons)):
                if j != index:  # Don't calculate force on itself (NaN).
                    i = list_electrons[j]
                    parallel_force_sum += ((single_electron.y - i.y) / ((i.x - single_electron.x)**2 + (i.y - single_electron.y)**2)**1.5)
        # For clarity the partial sums are either cos(phi) / r^2,
        # which equals (x1 - x2)/sqrt((x1 - x2)^2 + (y1 - y2)^2)^3.
        # Of course if force has to be parallel to y replace cos with sin.
        return parallel_force_sum

    # Calculate new coordinates
    if abs(list_electrons[index].y) == 1:  # Move in x direction.
        new_x = (list_electrons[index].x +
                 forces_on_electron(index, list_electrons) /
                 len(list_electrons)**2 / 10)
        # Factor 100 is completely arbitrary.
        # Move only incrementally and regarding density of electrons.
        if new_x > 1:  # Keep electrons on the square.
            new_x = 1
        elif new_x < -1:  # Keep electrons on the square.
            new_x = -1
        return Electron(new_x, list_electrons[index].y)
    else:
        new_y = (list_electrons[index].y +
                 forces_on_electron(index, list_electrons) /
                 len(list_electrons)**2 / 10)
        # Factor 100 is completely arbitrary.
        # Move only incrementally and regarding density of electrons.
        if new_y > 1:  # Keep electrons on the square.
            new_y = 1
        elif new_y < -1:  # Keep electrons on the square.
            new_y = -1
        return Electron(list_electrons[index].x, new_y)


def limit_function(list_old, list_new):
    # Accepts old and new iteration of electron
    # distribution in the form of two lists
    # containing Electron objects.
    # Returns True if electrons are sufficiently
    # close to their equillibrium.
    # This happens when two successive steps of simulation
    # lead to sufficiently similar end positions.

    no_electrons = len(list_old)
    sum_of_differences = 0
    for i in range(no_electrons):
        sum_of_differences += (abs(list_old[i].x - list_new[i].x) +
                               abs(list_old[i].y - list_new[i].y))
    if sum_of_differences < 0.0001 * no_electrons:
        # 0.0001 is an arbitrary threshold.
        return True
    else:
        return False


def introduce_perturbations(list_electrons):
    # Gets list of Electron objects as input
    # and returns list of Electron objects which
    # are slighly randomly translated from their
    # original positions.
    # It depends on pseudorandom module 'random'
    # which is random enough for this purpose as
    # the probability of perturbing the whole system
    # into another unstable equillibrium is very low.

    new_list = []
    for i in range(len(list_electrons)):
        perturbation = (random() - 0.5) / len(list_electrons) / 100
        # Factor 100 is completely arbitrary.
        if abs(list_electrons[i].x) == 1:  # Move in y-direction.
            new_y = list_electrons[i].y + perturbation
            if new_y < -1:
                new_y = -1
            elif new_y > 1:
                new_y = 1
            new_list.append(Electron(list_electrons[i].x,
                                     new_y))
        else:  # Move in x-direction
            new_x = list_electrons[i].x + perturbation
            if new_x < -1:
                new_x = -1
            elif new_x > 1:
                new_x = 1
            new_list.append(Electron(new_x,
                                     list_electrons[i].y))

    # Make sure electrons are sufficiently perturbed.
    if not limit_function(list_electrons, new_list):
        return introduce_perturbations(new_list)
    else:
        return new_list


def save_image(list_electrons, step):
    # Gets list of Electron objects, step number
    # Creates correct directory structure
    # and saves an image to it.

    # Create directories.
    no_electrons = len(list_electrons)
    system('mkdir -p ./data/stored-states/{}-electrons/images/'
           .format(no_electrons))

    # Create image.
    plt.clf()
    plt.axis('equal')
    plt.plot([1, -1, -1, 1, 1], [1, 1, -1, -1, 1], color='black', alpha=0.7)
    plt.plot([i.x for i in list_electrons], [i.y for i in list_electrons],
                'b.')
    plt.title('Step ' + str(step))
    plt.suptitle('{} electrons'.format(no_electrons))
    plt.tick_params(which='both',       # Both major and minor ticks are affected.
                    bottom=False,       # Ticks along the bottom edge are off.
                    left=False,         # Ticks along the left edge are off.
                    labelbottom=False,  # Labels along the bottom edge are off.
                    labelleft=False)    # Labels along the left edge are off.
    # Save image.
    plt.savefig('./data/stored-states/{}-electrons/images/image-{:0>3}.png'
                .format(no_electrons, step))


def run_simulation(no_electrons, max_tries, images=False):
    #   - graph with original distribution overlayed with equillibrium
    #   - graph with total potential energy over time
    #   - graph with total distance over time
    #   - graph with average distance over time
    #   - graph of equillibrium electric field around the square
    #   - graph of starting state electric field around the square
    #   - graph of overlayed both electric fields

    # Gets number of electrons, maximum number of steps, and bools
    # Runs the simulation until limit_function returns True.
    # Then calls introduce_perturbations to nudge the system
    # out of its potential unstable equillibrium and runs the
    # simulation again until limit_funtion return True.
    # If the electrons are positioned close enough (limit_function)
    # in the second run of simulation, graphs are drawn.
    # On users decision images are created, from which .gifs
    # can be made.

    list_electrons_original = []
    # Uniformly distribute electrons over 2pi angle. Start at the corner.
    for i in range(no_electrons):
        list_electrons_original.append(
            put_electron_on_a_square(2 * np.pi * i / no_electrons + np.pi/4))

    # Work on separate lists so original is left untouched.
    list_electrons = introduce_perturbations(list_electrons_original)
    new_electrons = [i for i in list_electrons_original]

    # Run simulation.
    for i in range(max_tries):
        if i == max_tries - 1:
            print('Warning: MAX STEPS REACHED!')
        if images:
            save_image(new_electrons, i)
        for j in range(no_electrons):
            new_electrons[j] = correct_position(j, list_electrons)
        if limit_function(list_electrons, new_electrons):
            # Electrons are close enough to equillibrium.
            break
        else:
            # Assign new values and continue the loop.
            list_electrons = [i for i in new_electrons]

    # Duplicate new_electrons list.
    first_equillibrium = [i for i in new_electrons]

    # Perturb the system.
    list_electrons = introduce_perturbations(new_electrons)

    # Rerun simulation until perturbations have no effect on end positions.
    equillibrium_one = [i for i in first_equillibrium]
    equillibrium_two = [i for i in list_electrons]
    tries = 0
    while not limit_function(equillibrium_one, equillibrium_two) and tries < 10:
        # Realistically there should be at most 3 or 4 tries.
        tries += 1
        for i in range(max_tries):
            for j in range(no_electrons):
                new_electrons[j] = correct_position(j, list_electrons)
            if limit_function(list_electrons, new_electrons):
                # Electrons are close enough to equillibrium.
                break
            else:
                # Assign new values and continue the loop.
                list_electrons = [i for i in new_electrons]
                # list_electrons = introduce_perturbations(new_electrons)
        equillibrium_two = [i for i in equillibrium_one]
        equillibrium_one = [i for i in new_electrons]

    # Output equillibrium distribution of electrons and the starting one.
    return new_electrons, list_electrons_original


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


# Find the equillibrium state.
# equillibrium_state, starting_state = run_simulation(120, 600, False, False)
