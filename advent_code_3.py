import re
import numpy as np



with open('input.txt', 'r') as f:
	d = f.readlines()


numbers = [str(i) for i in range(10)]

symbols = set([s for r in d for s in r if not s in (numbers + ['.', '\n'])])


rows = []
for e, row in enumerate(d):
	row = row.replace('\n', '')

	# Get positions of stars
	stars_positions = sorted([i.start() for i in re.finditer(re.escape('*'), row)])

	# Get positions of symbols
	s_positions = sorted([i.start() for s in symbols for i in re.finditer(re.escape(s), row)])

	# Get numbers with start and end positions
	nb_positions = {}

	# REDO the split with no error
	e_nb, is_nb, cur = 0, False, ''
	while e_nb<len(row):
		c = row[e_nb]
		if c in numbers:
			is_nb = True
			cur = cur + c
		else:
			if is_nb:
				nb_positions[(e_nb - len(cur), e_nb)] = int(cur)
				is_nb, cur = False, ''
		e_nb += 1

	if is_nb:
		nb_positions[(e_nb - len(cur), e_nb)] = int(cur)

	rows.append((s_positions, nb_positions, stars_positions))


total = 0
for e, (s_positions, nb_positions, stars_positions) in enumerate(rows):
	for s in stars_positions:
		nb_adj, mult = 0, 1
		for d in [nb_positions, rows[e-1][1] if e>0 else {}, rows[e+1][1] if e<len(rows)-1 else {}]:
			for (i1, i2), nb in d.items():
				if min([abs(s - i) for i in range(i1-1, i2+1)])==0:
					nb_adj += 1
					mult *= nb

		if nb_adj==2:
			total += mult

print(total)