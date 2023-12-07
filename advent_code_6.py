import re
import numpy as np
from tqdm import tqdm

with open('input.txt', 'r') as f:
    d = f.readlines()

###
# Part 1
###

times = list(map(int, d[0][:-1].split(':')[1].split()))
distances = list(map(int, d[1].split(':')[1].split()))


def get_distances(t):
    return [i * (t - i) for i in range(t + 1)]


mult = 1
for t, d in zip(times, distances):
    dist = get_distances(t)
    nb = len([i for i in dist if i > d])
    mult *= nb

print(mult)

###
# Part 2
###

time = int(d[0][:-1].split(':')[1].replace(' ', ''))
distance = int(d[1].split(':')[1].replace(' ', ''))


def get_distances(t):
    return [i * (t - i) for i in range(t + 1)]


distances = get_distances(time)

print((np.array(distances) >= distance).sum())
