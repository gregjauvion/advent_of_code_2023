from tqdm import tqdm
import numpy as np


with open('input.txt', 'r') as f:
    d = f.readlines()

d = [i.replace('\n', '') for i in d]

sequence = d[0]

paths = {}
for s in d[2:]:
    p1, p2 = s.split(' = ')
    paths[p1] = p2[1:-1].split(', ')


###
# Part 1
###

start = 'AAA'
for e in range(1000):
    for s in sequence:
        start = paths[start][0] if s=='L' else paths[start][1]

    if start=='ZZZ':
        break

print(len(sequence) * (e + 1))



###
# Part 2
###


def get_seq(n):
    """ Returns the sequence upto the first repetition."""

    n_path = [n]

    # Get upto the first repetition
    for e in range(1000):
        for s in sequence:
            n = paths[n][0] if s=='L' else paths[n][1]

        cycle = n in n_path
        n_path.append(n)
        if cycle:
            break

    end_z_idx = [e for e, i in enumerate(n_path) if i[-1] == 'Z'][0]
    i1, i2 = n_path[:-1].index(n_path[-1]), len(n_path) - 1
    #get_idx = lambda e: e if e < i1 else i1 + (e - i1) % (i2 - i1)

    return n_path, end_z_idx, i2 - i1

# Generate list of indices that end with Z for every start node
starts = [n for n in paths.keys() if n[-1]=='A']
n_paths = [get_seq(n) for n in starts]

diffs = [i[2] for i in n_paths]
print(len(sequence) * np.product(diffs))