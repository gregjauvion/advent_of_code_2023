import numpy as np
from tqdm import tqdm


with open('input.txt', 'r') as f:
    d = [i.strip() for i in f.readlines()]

data = np.array([list(i) for i in d])

m1 = {'right': 'up', 'left': 'down', 'up': 'right', 'down': 'left'}
m2 = {'right': 'down', 'left': 'up', 'up': 'left', 'down': 'right'}

def update(i, j, direction):

    if direction=='right':
        i_, j_ = i, j + 1
    elif direction=='left':
        i_, j_ = i, j - 1
    elif direction=='up':
        i_, j_ = i - 1, j
    elif direction=='down':
        i_, j_ = i + 1, j

    valid = (0 <= i_ < data.shape[0]) and (0 <= j_ < data.shape[1])
    if not valid:
        return []

    s = data[i_, j_]
    directions = []
    if s=='.':
        directions = [direction]
    elif s=='/':
        directions = [m1[direction]]
    elif s=='\\':
        directions = [m2[direction]]
    elif s=='-':
        if direction in ['left', 'right']:
            directions = [direction]
        else:
            directions = ['left', 'right']
    elif s=='|':
        if direction in ['up', 'down']:
            directions = [direction]
        else:
            directions = ['up', 'down']

    return [(i_, j_, d) for d in directions]


###
# Part 1
###

energized = np.zeros(data.shape)
directions = [(0, -1, 'right')]
patience = 5
nb_energized, e_patience = -1, 0
while (energized.sum()>nb_energized) or (e_patience<patience):
    if nb_energized!=energized.sum():
        nb_energized = energized.sum()
        e_patience = 0
    else:
        e_patience += 1

    # Get new positions
    directions = [d for i, j, direction in directions for d in update(i, j, direction)]

    for i, j, d in directions:
        energized[i, j] = 1

print(energized.sum())


###
# Part 2
###

ij_value = {}
for i_init in tqdm(range(data.shape[0])):
    dir_init = [[(i_init, -1, 'right')], [(i_init, data.shape[1], 'left')],
                [(-1, i_init, 'down')], [(data.shape[0], i_init, 'up')]]
    for i_directions in dir_init:
        directions = i_directions
        energized = np.zeros(data.shape)
        patience = 5
        nb_energized, e_patience = -1, 0
        while (energized.sum()>nb_energized) or (e_patience<patience):
            if nb_energized!=energized.sum():
                nb_energized = energized.sum()
                e_patience = 0
            else:
                e_patience += 1

            # Get new positions
            directions = [d for i, j, direction in directions for d in update(i, j, direction)]

            for i, j, d in directions:
                energized[i, j] = 1

        ij_value[tuple(i_directions)] = energized.sum()

print(max(ij_value.values()))