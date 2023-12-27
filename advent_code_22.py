import numpy as np

with open('input_test.txt', 'r') as f:
	d = [i.strip() for i in f.readlines()]


# Compute the maximum shape on every dimension
x_max, y_max, z_max = 0, 0, 0
for r in d:
	start, end = [i.split(',') for i in r.split('~')]
	x_max = max(x_max, int(start[0]), int(end[0]))
	y_max = max(y_max, int(start[1]), int(end[1]))
	z_max = max(z_max, int(start[2]), int(end[2]))


# Fill the bricks in a 3D array
# Every brick is represented by an index from 1 to {nb_bricks}
data = np.zeros((x_max + 1, y_max + 1, z_max + 1))
for e_r, r in enumerate(d):
	start, end = [i.split(',') for i in r.split('~')]
	start, end = [int(i) for i in start], [int(i) for i in end]
	start[2] -= 1
	end[2] -= 1

	if start[0]!=end[0]:
		for c in range(start[0], end[0]):
			data[c, start[1], start[2]] = e_r + 1

	if start[1]!=end[1]:
		for c in range(start[1], end[1]):
			data[start[0], c, start[2]] = e_r + 1

	if start[2]!=end[2]:
		for c in range(start[2], end[2]):
			data[start[0], start[1], c] = e_r + 1


# Make them fall
for e in range(1, len(d) + 1):
	# Get the indices for this brick
	w = np.where(data==e)

	# Make it fall step by step until it can no more
	z_min = min(w[2])
	while z_min>0:
		if (data[w[0], w[1], w[2] - 1]==0).all():
			# The previous step if empty, the brick can fall one more step
			z_min -= 1
			data[w[0], w[1], w[2]] = 0

			w = (w[0], w[1], w[2] - 1)
			data[w[0], w[1], w[2]] = e
			
		else:
			# The brick can not fall anymore
			break
			

for i in range(9):
	plt.imshow(data[:,:,i]) ; plt.colorbar() ; plt.show()


# For each brick check if it can be disintegrated
for e in range(1, len(d) + 1):
	w = np.where(data==e)
	other = [i for i in set(data[w[0], w[1], w[2] + 1]) if i!=0]
	if len(other)>0:
		print(e, other)



