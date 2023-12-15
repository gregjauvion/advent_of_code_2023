import numpy as np

with open('input_test.txt', 'r') as f:
    d = np.array([list(i.strip()) for i in f.readlines()])

###
# Part 1
###

for c in range(d.shape[1]):
    d[:, c] = list('#'.join([''.join(sorted(list(i), reverse=True)) for i in ''.join(d[:, c]).split('#')]))

print(np.sum((d=='O').sum(axis=1) * np.arange(d.shape[0], 0, -1)))


###
# Part 2
###

def north(d):
    for c in range(d.shape[1]):
        d[:, c] = list(
            '#'.join([
                ''.join(sorted(list(i), reverse=True)) for i in ''.join(d[:, c]).split('#')
            ])
        )

def south(d):
    for c in range(d.shape[1]):
        d[:, c] = list(
            '#'.join([
                ''.join(sorted(list(i), reverse=False)) for i in ''.join(d[:, c]).split('#')
            ])
        )

def west(d):
    for c in range(d.shape[0]):
        d[c, :] = list(
            '#'.join([
                ''.join(sorted(list(i), reverse=True)) for i in ''.join(d[c, :]).split('#')
            ])
        )

def east(d):
    for c in range(d.shape[0]):
        d[c, :] = list(
            '#'.join([
                ''.join(sorted(list(i), reverse=False)) for i in ''.join(d[c, :]).split('#')
            ])
        )

def cycle(d):
    north(d)
    west(d)
    south(d)
    east(d)


with open('input.txt', 'r') as f:
    d = np.array([list(i.strip()) for i in f.readlines()])

# Do cycles until two similar states are found
tmp = {}
e = 0
for e in range(1000000):
    cycle(d)
    h = hash(d.tostring())
    if h in tmp:
        e_start = tmp[h]
        break
    tmp[h] = e

# Compute number of cycles to run
nb_cycles = (1E9 - 1 - e_start) % (e - e_start)
for i in range(int(nb_cycles)):
    cycle(d)

print(np.sum((d=='O').sum(axis=1) * np.arange(d.shape[0], 0, -1)))
