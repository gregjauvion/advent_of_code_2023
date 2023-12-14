import matplotlib.pyplot as plt
import numpy as np

def next(before, current, symbol):

    dy, dx = current[0] - before[0], current[1] - before[1]

    if symbol=='.':
        return None

    # Check if in-pipes are True
    if symbol=='|':
        return (current[0] + dy, current[1]) if abs(dy)==1 else None
    elif symbol=='-':
        return (current[0], current[1] + dx) if abs(dx)==1 else None
    elif symbol=='L':
        if dy==1:
            return (current[0], current[1] + 1)
        elif dx==-1:
            return (current[0] - 1, current[1])
        else:
            return None
    elif symbol=='J':
        if dy==1:
            return (current[0], current[1] - 1)
        elif dx==1:
            return (current[0] - 1, current[1])
        else:
            return None
    elif symbol=='7':
        if dx==1:
            return (current[0] + 1, current[1])
        elif dy==-1:
            return (current[0], current[1] - 1)
        else:
            return None
    elif symbol=='F':
        if dy==-1:
            return (current[0], current[1] + 1)
        elif dx==-1:
            return (current[0] + 1, current[1])
        else:
            return None


with open('input.txt', 'r') as f:
    grid = [i.strip() for i in f.readlines()]


###
# Part 1
###

s_y = [e for e, i in enumerate(grid) if 'S' in i][0]
s_x = grid[s_y].index('S')

starts = [(s_y + 1, s_x), (s_y - 1, s_x), (s_y, s_x + 1), (s_y, s_x - 1)]
cycle = []
for s in starts:
    cycle = [s]
    before, cur = (s_y, s_x), s
    nb = 1
    while cur!=(s_y, s_x):
        n = next(before, cur, grid[cur[0]][cur[1]])
        cycle.append(n)
        nb += 1
        if n is not None:
            before, cur = cur, n
        else:
            break

    if cur==(s_y, s_x):
        print(f'Cycle found, {cur}, {nb}')
        break
    else:
        print('No cycle found.')

plt.plot([i[1] for i in cycle], [i[0] for i in cycle]) ; plt.show()


###
# Part 2
###

# is_inside is an array that contains the interior/exterior of the maze
# -1 means unknown
# 0 means outside
# 1 means inside
# 2 means the border
is_inside = np.zeros((len(grid), len(grid[0])), dtype=int) - 1


# 1st step:
# Loop on the cycle and update the sets of inside and outside points neighbors to the maze
s_cycle = set(cycle)
before, current = cycle[0], cycle[1]
inside_direction = 'down'
insides, outsides = {(current[0] - 1, current[1])}, {(current[0] + 1, current[1])}
for next in cycle[2:]:
    dy, dx = current[0] - before[0], current[1] - before[1]
    dy2, dx2 = next[0] - current[0], next[1] - current[1]
    if dx==1:
        if dx2==1:
            pass
        elif dy2==1:
            inside_direction = 'right' if inside_direction=='up' else 'left'
        elif dy2==-1:
            inside_direction = 'left' if inside_direction == 'up' else 'right'
    elif dx==-1:
        if dx2==-1:
            pass
        elif dy2==1:
            inside_direction = 'left' if inside_direction=='up' else 'right'
        elif dy2==-1:
            inside_direction = 'right' if inside_direction == 'up' else 'left'
    elif dy==-1:
        if dy2==-1:
            pass
        elif dx2==1:
            inside_direction = 'up' if inside_direction == 'left' else 'down'
        elif dx2==-1:
            inside_direction = 'down' if inside_direction == 'left' else 'up'
    elif dy==1:
        if dy2==1:
            pass
        elif dx2==-1:
            inside_direction = 'up' if inside_direction == 'left' else 'down'
        elif dx2==1:
            inside_direction = 'down' if inside_direction == 'left' else 'up'

    for tmp in [current, next]:
        if inside_direction=='up':
            insides.add((tmp[0] - 1, tmp[1]))
            outsides.add((tmp[0] + 1, tmp[1]))
        elif inside_direction=='down':
            insides.add((tmp[0] + 1, tmp[1]))
            outsides.add((tmp[0] - 1, tmp[1]))
        elif inside_direction=='left':
            insides.add((tmp[0], tmp[1] - 1))
            outsides.add((tmp[0], tmp[1] + 1))
        elif inside_direction=='right':
            insides.add((tmp[0], tmp[1] + 1))
            outsides.add((tmp[0], tmp[1] - 1))

    before, current = current, next

# Remove points in the cycle from the insides and outsides sets
s_cycle = set(cycle)
l_insides = [i for i in insides if (not i in s_cycle) and (0<=i[0]<is_inside.shape[0]) and (0<=i[1]<is_inside.shape[1])]
l_outsides = [i for i in outsides if (not i in s_cycle) and (0<=i[0]<is_inside.shape[0]) and (0<=i[1]<is_inside.shape[1])]

# Update is_inside array
for y, x in l_insides:
    is_inside[y, x] = 1

for y, x in l_outsides:
    is_inside[y, x] = 0

for y, x in cycle:
    is_inside[y, x] = 2


# 2nd step:
# For every inside/outside point, label their neighbours similarly
def grow(point, label):
    y, x = point
    is_inside[y, x] = label
    neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
    for n_y, n_x in neighbors:
        if 0<=n_y<is_inside.shape[0] and 0<=n_x<is_inside.shape[1] and is_inside[n_y, n_x]==-1:
            grow((n_y, n_x), label)

for point in l_insides:
    grow(point, 1)

for point in l_outsides:
    grow(point, 0)

plt.imshow(is_inside) ; plt.colorbar() ; plt.show()

print((is_inside==1).sum())
