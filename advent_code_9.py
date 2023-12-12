import numpy as np


with open("input.txt", "r") as f:
	data = f.readlines()


###
# Part 1
###

result = 0
for row in data:
	z = np.array([int(i) for i in row.strip().split()])

	p = z[-1]
	while (z!=0).sum() > 0:
		z = z[1:] - z[:-1]
		p += z[-1]

	print(p)
	result += p

print(result)


###
# Part 2
###

result = 0
for row in data:
	z = np.array([int(i) for i in row.strip().split()])

	e = 0
	p = z[0]
	while (z!=0).sum() > 0:
		z = z[1:] - z[:-1]
		e += 1
		p += (-1)**e * z[0]

	print(p)
	result += p

print(result)