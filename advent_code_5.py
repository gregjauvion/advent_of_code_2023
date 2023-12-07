import re
import numpy as np
from tqdm import tqdm

with open('input.txt', 'r') as f:
    d = f.read()

ds = d.split('\n\n')


###
# Part 1
###


def get_map(ranges, v):
    for dest, source, nb in ranges:
        if source <= v < source + nb:
            return v + dest - source

    return v


seeds = [int(s) for s in ds[0].split(': ')[1].split(' ')]
maps = [[list(map(int, k.split(' '))) for k in i.split('\n')[1:]] for i in ds[1:]]

min_s = np.inf
for s in seeds:
    for m in maps:
        s = get_map(m, s)
    print(s)

    if s < min_s:
        min_s = s

print(min_s)


###
# Part 2
###


def get_map_v(ranges, seeds):
    is_ret = np.zeros(seeds.shape[0], dtype=np.bool)
    for dest, source, nb in ranges:
        is_impacted = (seeds >= source) & (seeds < source + nb)
        if (is_impacted & ~is_ret).sum() > 0:
            seeds[(is_impacted & ~is_ret)] += dest - source
            is_ret = is_ret | is_impacted

    return seeds


maps = [[list(map(int, k.split(' '))) for k in i.split('\n')[1:]] for i in ds[1:]]

seeds_ = [int(i) for i in ds[0].split(': ')[1].split(' ')]
min_s = np.inf
for i in tqdm(range(len(seeds_) // 2)):
    s, n = seeds_[2 * i], seeds_[2 * i + 1]
    seeds = np.arange(s, s + n)

    for m in tqdm(maps):
        seeds = get_map_v(m, seeds)

    m = seeds.min()
    if m < min_s:
        min_s = m

print(min_s)
