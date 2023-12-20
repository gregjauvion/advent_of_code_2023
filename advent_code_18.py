from shapely.geometry import Polygon, Point, box
from tqdm import tqdm


with open('input_test.txt', 'r') as f:
    data = [i.strip().split(' ') for i in f.readlines()]


def build_coords(directions):

    # Start from start and get polygon coordinates
    cur = (0, 0)
    points = [cur]
    for d, n in directions:
        if d=='R':
            cur_ = (cur[0], cur[1] + n)
        elif d=='L':
            cur_ = (cur[0], cur[1] - n)
        elif d=='U':
            cur_ = (cur[0] - n, cur[1])
        elif d=='D':
            cur_ = (cur[0] + n, cur[1])

        points.append(cur_)
        cur = cur_

    return points


###
# Part 1
###

points = build_coords([(d, int(n)) for d, n, _ in data])
polygon = Polygon(points)
print(polygon.area + polygon.length // 2 + 1)


###
# Part 2
###

mapping = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
directions = []
for _, _, h in data:
    dir_ = mapping[int(h[-2])]
    nb = int(h[-7:-2], 16)
    directions.append((dir_, nb))

points = build_coords(directions)
polygon = Polygon(points)
print(polygon.area + polygon.length // 2 + 1)
