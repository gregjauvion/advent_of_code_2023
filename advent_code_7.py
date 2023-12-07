import numpy as np
from collections import Counter


TYPES = {
	'five': 6,
	'four': 5,
	'full': 4,
	'three': 3,
	'two_pairs': 2,
	'one_pair': 1,
	'high_card': 0
}

CARD_VALUE = {
	'A': 12,
	'K': 11,
	'Q': 10,
	'J': 9,
	'T': 8,
	'9': 7,
	'8': 6,
	'7': 5,
	'6': 4,
	'5': 3,
	'4': 2,
	'3': 1,
	'2': 0
}

CARD_VALUE_2 = {
	'A': 12,
	'K': 11,
	'Q': 10,
	'T': 9,
	'9': 8,
	'8': 7,
	'7': 6,
	'6': 5,
	'5': 4,
	'4': 3,
	'3': 2,
	'2': 1,
	'J': 0,
}


def get_type(hand, part_2):

	counts = Counter(hand)

	# For Part 2, we replace J by the most frequent card
	if part_2:
		counts_wo_j = {i: j for i, j in counts.items() if i!='J'}
		if len(counts_wo_j)>0:
			nb_max = max(counts_wo_j.values())
			for i, j in counts_wo_j.items():
				if (j==nb_max) and (i!='J'):
					counts[i] += counts['J']
					counts['J'] = 0
					break

	sorted_values = np.array(sorted(counts.values()))[::-1]

	if sorted_values[0]==5:
		return TYPES['five']
	elif sorted_values[0]==4:
		return TYPES['four']
	elif sorted_values[0]==3 and sorted_values[1]==2:
		return TYPES['full']
	elif sorted_values[0]==3:
		return TYPES['three']
	elif sorted_values[0]==2 and sorted_values[1]==2:
		return TYPES['two_pairs']
	elif sorted_values[0]==2:
		return TYPES['one_pair']
	else:
		return TYPES['high_card']


def compare_cards(hand_1, hand_2, part_2):

	for c1, c2 in zip(hand_1, hand_2):
		if part_2:
			v1, v2 = CARD_VALUE_2[c1], CARD_VALUE_2[c2]
		else:
			v1, v2 = CARD_VALUE[c1], CARD_VALUE[c2]

		if v1!=v2:
			return 1 if v2>v1 else 0

	raise Exception("Same hands in compare_cards.")


def compare_hands(hand_1, hand_2, part_2=False):

	t1, t2 = get_type(hand_1, part_2), get_type(hand_2, part_2)
	if t1 != t2:
		return 1 if t2>t1 else 0
	else:
		return compare_cards(hand_1, hand_2, part_2)




with open('input.txt', 'r') as f:
	d = f.readlines()

hands_bids = [i.replace('\n', '').split(' ') for i in d]
hands = [i[0] for i in hands_bids]
bids = np.array([int(i[1]) for i in hands_bids])


sorted_indices = []
for i in range(len(hands)):
	hand = hands[i]
	
	e = 0
	while e<len(sorted_indices) and compare_hands(hand, hands[sorted_indices[e]], part_2=True)==1:
		e += 1

	sorted_indices.insert(e, i)


print(np.sum(bids[sorted_indices] * np.arange(1, len(sorted_indices) + 1)[::-1]))
