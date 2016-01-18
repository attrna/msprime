"""
Simple client code for development purposes.
"""

from __future__ import print_function
from __future__ import division

import math

import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

import msprime

def mutations():
    recomb_rates = [(10, 0.05), (20, 0.1), (30, 0), (40, 0.05)]
    for x, rate in recomb_rates:
        print(x, rate)
    max_rate = max(rate for _, rate in recomb_rates)
    print("max_ rate = ", max_rate)

    tree_sequence = msprime.simulate(10, 100, max_rate, random_seed=1)
    for tree in tree_sequence.trees():
        print(tree.get_interval())


def physical_to_genetic(x, recomb_rates):
    s = 0
    last_phys_x = 0
    j = 0
    while j < len(recomb_rates) and x > recomb_rates[j][0]:
        phys_x, recomb_rate = recomb_rates[j]
        s += (phys_x - last_phys_x) * recomb_rate
        j += 1
        last_phys_x = phys_x
    if x != last_phys_x:
        _, recomb_rate = recomb_rates[j]
        s += (x - last_phys_x) * recomb_rate
    return s


def genetic_to_physical(x, recomb_rates):
    s = 0
    last_phys_x = 0
    j = 0
    while j < len(recomb_rates) and s < x:
        phys_x, recomb_rate = recomb_rates[j]
        s += (phys_x - last_phys_x) * recomb_rate
        j += 1
        last_phys_x = phys_x
    y = last_phys_x
    if x != s:
        y -= (s - x) / recomb_rate
    return y


def plot_distance_maps(recomb_rates):
    # Plot the piecewise map of physical distance to recombination rate
    x = np.zeros(2 * len(recomb_rates))
    y = np.copy(x)
    last_phys_x = 0
    j = 0
    for phys_x, recomb_rate in recomb_rates:
        x[j] = last_phys_x
        y[j] = recomb_rate
        j += 1
        x[j] = phys_x
        y[j] = recomb_rate
        last_phys_x = phys_x
        j += 1
    pyplot.plot(x, y)
    pyplot.ylim(-0.01, 1.01)
    pyplot.savefig("phys_recomb_rate.png")

    pyplot.clf()

    x = np.zeros(1 + len(recomb_rates))
    y = np.copy(x)
    j = 1
    s = 0
    last_phys_x = 0
    for phys_x, recomb_rate in recomb_rates:
        s += (phys_x - last_phys_x) * recomb_rate
        y[j] = s
        x[j] = phys_x
        j += 1
        last_phys_x = phys_x
    pyplot.plot(x, y)
    # physical_dist = 21.6
    # genetic_dist = physical_to_genetic(physical_dist, recomb_rates)
    genetic_dist = 4
    physical_dist = genetic_to_physical(genetic_dist, recomb_rates)
    pyplot.axvline(x=physical_dist, color="green")
    pyplot.axhline(y=genetic_dist, color="green")
    pyplot.savefig("phys_genetic_distance.png")


def plot_1kg_map():
    infile = "tmp__NOBACKUP__/genetic_map_b36/genetic_map_chr1_b36.txt.gz"

    import pandas as pd
    df = pd.read_csv(infile, delim_whitespace=True, compression="gzip",
            names=["pos", "rate", "distance"], header=0)
    # print(df.pos)
    physical_length = df.pos.iloc[-1]
    num_crossovers = df.distance.iloc[-1] / 100
    Ne = 10**4
    rate = 4 * Ne * num_crossovers / physical_length
    print("Overall rate = {:.2E}".format(rate))

    scaled_rate = np.array(4 * Ne * (df.rate / 100) / 10**6)[:-1]
    print(scaled_rate)

    lengths = np.diff(df.pos)
    print(lengths)

    print(lengths * scaled_rate)


    # print("overall rate = ",
    # print(df["pos"])
    # pyplot.plot(df.pos, df.rate)
    # pyplot.savefig("1kg.png")



if __name__ == "__main__":
    # mutations()

    # plot_distance_maps(
    #     [(10, 0.1), (11, 1), (20, 0.1), (21, 1), (30, 0.1)]
    # )
    plot_1kg_map()

