import re
import numpy as np

with open('input.txt', 'r') as f:
    d = f.readlines()

for e, row in enumerate(d):
    row = row.replace('\n', '')

    cards, winning = row.split(': ')[1].split(' | ')
    cards = set([int(i.replace(' ', '')) for i in cards.split(' ') if i.replace(' ', '') != ''])
    wins = set([int(i.replace(' ', '')) for i in winning.split(' ') if i.replace(' ', '') != ''])

    nb_wins = len(wins.intersection(cards))
    if nb_wins > 0:
        nb = 2 ** (nb_wins - 1)
        print(nb)
        total += nb

print(total)

with open('input.txt', 'r') as f:
    d = f.readlines()

nb_wins = []
for e, row in enumerate(d):
    row = row.replace('\n', '')

    cards, winning = row.split(': ')[1].split(' | ')
    cards = set([int(i.replace(' ', '')) for i in cards.split(' ') if i.replace(' ', '') != ''])
    wins = set([int(i.replace(' ', '')) for i in winning.split(' ') if i.replace(' ', '') != ''])

    nb_wins.append(len(wins.intersection(cards)))

nb_cards = {e: 0 for e in range(len(rows))}
for e, nb_win in enumerate(nb_wins):

    for i in range(1, row + 1):
        if e + i < len(nb_cards):
            nb_cards[e + i] += nb_cards[e] + 1

    nb_cards[e] += 1

print(sum(nb_cards.values()))
