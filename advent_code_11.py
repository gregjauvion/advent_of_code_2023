import numpy as np

with open('input.txt', 'r') as f:
    data = np.array([[i for i in s.strip()] for s in f.readlines()])


###
# Part 1
###

def expand(data):

    # Insert rows
    rows_to_expand = np.where((data=='.').all(axis=1))[0]
    r_to_insert = np.array(['.' for _ in range(data.shape[1])])
    data_ = np.insert(data, rows_to_expand, r_to_insert, axis=0)

    # Insert columns
    cols_to_expand = np.where((data=='.').all(axis=0))[0]
    c_to_insert = np.array(['.' for _ in range(data_.shape[0])])[:, None]
    data_ = np.insert(data_, cols_to_expand, c_to_insert, axis=1)

    return data_


d_expanded = expand(data)

ys, xs = np.where(d_expanded=='#')
i_yx = {e: (y, x) for e, (y, x) in enumerate(zip(ys, xs))}
inds = sorted(i_yx.keys())

dist = 0
for e1, i1 in enumerate(inds):
    for i2 in inds[e1+1:]:
        y1, x1 = i_yx[i1]
        y2, x2 = i_yx[i2]
        dist += max(y1, y2) - min(y1, y2) + max(x1, x2) - min(x1, x2)

print(dist)


###
# Part 2
###

# Build the grid as a sparse matrix
matrix = {}
ys, xs = np.where(data=='#')
for y, x in zip(ys, xs):
    matrix[y, x] = 1

# Expand rows and columns
nb = 1E6 - 1
rows_to_expand = np.where((data=='.').all(axis=1))[0]
cols_to_expand = np.where((data=='.').all(axis=0))[0]
matrix_exp = {}
for (y, x), v in matrix.items():
    y_exp = y + nb * np.searchsorted(rows_to_expand, y, side='right')
    x_exp = x + nb * np.searchsorted(cols_to_expand, x, side='right')
    matrix_exp[(y_exp, x_exp)] = 1

# Compute distances
i_yx = {e: (y, x) for e, (y, x) in enumerate(matrix_exp.keys())}
inds = sorted(i_yx.keys())
dist = 0
for e1, i1 in enumerate(inds):
    for i2 in inds[e1+1:]:
        y1, x1 = i_yx[i1]
        y2, x2 = i_yx[i2]
        dist += max(y1, y2) - min(y1, y2) + max(x1, x2) - min(x1, x2)

print(dist)