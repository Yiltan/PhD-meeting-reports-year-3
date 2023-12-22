import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from uncertainties import ufloat

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0"
    size_name = ("B", "KiB", "MiB", "GiB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (int(s), size_name[i])

def read_data(file_name):
    df = pd.read_csv(file_name)
    df = df.drop(columns=['Median', 'STD'])
    df = df.groupby(['Size']).agg(['mean', 'std']).reset_index()

    size = df['Size'].to_numpy()
    mean = df['Mean']['mean'].to_numpy()
    std = df['Mean']['std'].to_numpy()

    return size, mean, std

def plot_small():
    fig, ax = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(10)

    width = 0.25
    multiplier = 0

    # Bcast
    file_name = "bcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[:11]
    mean = mean[:11]
    std = std[:11]

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Bcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[:11]
    mean = mean[:11]
    std = std[:11]

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-parrived-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[:11]
    mean = mean[:11]
    std = std[:11]

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast + Parrived")
    multiplier += 1

    ax.set_ylabel('Latency ($\mu s$)')
    ax.set_xlabel('Buffer Size')

    x_labels = [ convert_size(s) for s in size]
    ax.set_xticks(x + width)
    ax.set_xticklabels(x_labels)
    ax.set_ylim(0)

    ax.legend(ncol=3, loc='upper left')

    plt.savefig("small_64.pdf", dpi=1000, bbox_inches='tight')
    plt.clf()

def plot_med():
    fig, ax = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(10)

    width = 0.25
    multiplier = 0

    # Bcast
    file_name = "bcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[11:18]
    mean = mean[11:18] / 1000.0
    std = std[11:18] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Bcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[11:18]
    mean = mean[11:18] / 1000.0
    std = std[11:18] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-parrived-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[11:18]
    mean = mean[11:18] / 1000.0
    std = std[11:18] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast + Parrived")
    multiplier += 1

    ax.set_ylabel('Latency (ms)')
    ax.set_xlabel('Buffer Size')

    x_labels = [ convert_size(s) for s in size]
    ax.set_xticks(x + width)
    ax.set_xticklabels(x_labels)
    ax.set_ylim(0)

    ax.legend(ncol=3, loc='upper left')

    plt.savefig("med_64.pdf", dpi=1000, bbox_inches='tight')
    plt.clf()

def plot_large():
    fig, ax = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(10)

    width = 0.25
    multiplier = 0

    # Bcast
    file_name = "bcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[18:]
    mean = mean[18:] / 1000.0
    std = std[18:] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Bcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[18:]
    mean = mean[18:] / 1000.0
    std = std[18:] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast")
    multiplier += 1

    # Pbcast
    file_name = "pbcast-parrived-p64-t32-n40.out"
    size, mean, std = read_data(file_name)
    size = size[18:]
    mean = mean[18:] / 1000.0
    std = std[18:] / 1000.0

    x = np.arange(len(size))
    y = mean
    yerr = std

    offset = width * multiplier
    rects = ax.bar(x + offset, y, width, yerr=yerr, label="Pbcast + Parrived")
    multiplier += 1

    ax.set_ylabel('Latency (ms)')
    ax.set_xlabel('Buffer Size')

    x_labels = [ convert_size(s) for s in size]
    ax.set_xticks(x + width)
    ax.set_xticklabels(x_labels)
    ax.set_ylim(0)

    ax.legend(ncol=3, loc='upper left')

    plt.savefig("large_64.pdf", dpi=1000, bbox_inches='tight')
    plt.clf()

plot_small()
plot_med()
plot_large()
