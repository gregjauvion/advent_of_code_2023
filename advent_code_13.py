import numpy as np


with open('input.txt', 'r') as f:
    d = f.read()

patterns = []
for p in d.split('\n\n'):
    patterns.append(np.array([list(i) for i in p.split('\n')]))


def get_score(p, diff=None):

    for row in range(1, p.shape[0]):
        nb_rows = min(row, p.shape[0] - row)
        up, down = p[row - nb_rows:row, :], p[row:row + nb_rows, :]
        if (up==down[::-1, :]).all():
            if (diff is None) or (diff!=row * 100):
                return row * 100

    for col in range(1, p.shape[1]):
        nb_cols = min(col, p.shape[1] - col)
        left, right = p[:, col - nb_cols:col], p[:, col:col + nb_cols]
        if (left==right[:, ::-1]).all():
            if (diff is None) or (diff != col):
                return col

    return None


###
# Part 1
###

score = 0
for p in patterns:
    score += get_score(p)

print(score)


###
# Part 2
###

def get_score_part_2(p):

    s1 = get_score(p)
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            p[i, j] = '.' if p[i, j]=='#' else '#'
            s = get_score(p, diff=s1)
            p[i, j] = '.' if p[i, j] == '#' else '#'
            if (s is not None):
                return s


score = 0
for p in patterns:
    score += get_score_part_2(p)

print(score)
