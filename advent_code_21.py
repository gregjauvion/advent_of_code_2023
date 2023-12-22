import numpy as np

with open('input.txt', 'r') as f:
    d = np.array([list(i.strip()) for i in f.readlines()])


start = np.where(d=='S')
x_start, y_start = start[0][0], start[1][0]


###
# Part 1
###

def grow(p):
    x, y = p
    n_p = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(x, y) for x, y in n_p if 0<=x<d.shape[0] and 0<=y<d.shape[1] and d[x, y]!='#']

points = {(x_start, y_start)}
for _ in range(64):
    points = set([i for p in points for i in grow(p)])

print(len(points))


###
# Part 2
###

def grow_v(data):
    """
    data is an array where: 0 means '.', 1 means '#', 2 means 'O'
    """

    points = np.array(np.where(data == 2)).T
    n_points = np.array([i for x, y in points for i in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]])
    n_points = n_points[(n_points[:, 0] >= 0) & (n_points[:, 0] < data.shape[0]) & (n_points[:, 1] >= 0) & (
                n_points[:, 1] < data.shape[1])]

    data[data==2] = 0
    data[n_points] = 2#np.where(data[n_points]==0, 2, 1)

    return data


data = np.where(d=='.', 0, np.where(d=='#', 1, 2))
for _ in range(64):
    data = grow_v(data)

print((data==2).sum())


