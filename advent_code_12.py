from collections import Counter


with open('input.txt', 'r') as f:
    data = [i.strip() for i in f.readlines()]


rows = []
for d in data:
    x, y = d.split(' ')
    rows.append((x, tuple([int(i) for i in y.split(',')])))


def get_splits(seq):
    """
    Split the sequence into several parts splitted by '.'
    """

    return tuple(s for s in seq.split('.') if s!='')


@functools.lru_cache(maxsize=1000000)
def compute_only_unknown(size, nbs):
    """
    Returns the number of possibilities if there are only '?'.
    """

    if len(nbs)==0:
        return 1
    elif len(nbs)==1:
        return max(0, size - nbs[0] + 1)
    else:
        ret = 0
        for i in range(nbs[0], size):
            ret += compute_only_unknown(size - i - 1, nbs[1:])

        return ret


@functools.lru_cache(maxsize=1000000)
def compute(splits: tuple, nbs: tuple):
    """
    Compute the number of possibilities.
    - {splits}: splits obtained after application of get_splits
    - {nbs}: list of numbers to match
    """

    if len(splits)==1:
        seq = splits[0]
        # If there is no '?', check if it matches {nbs}
        if not '?' in seq:
            return 1 if len(nbs)==1 and len(seq)==nbs[0] else 0
        elif Counter(seq)['?']==len(seq):
            return compute_only_unknown(len(seq), nbs)
        else:
            idx = seq.index('?')
            return compute(get_splits(seq[:idx] + '.' + seq[idx+1:]), nbs) + compute(get_splits(seq[:idx] + '#' + seq[idx+1:]), nbs)

    # Get the minimum number we have to build with the first split,
    # and the maximum number we can build.
    s = splits[0]
    len_0, len_1 = len(s), sum([len(i) for i in splits[1:]])
    nb_min, nb_max = sum(nbs) - len_1, len_0

    # Get the minimum and maximum number of elements from {nbs} we can use for the first split
    e_min, tot = len(nbs) - 1, sum(nbs)
    while e_min>=0:
        tot -= nbs[e_min]
        if tot<nb_min:
            break
        e_min -= 1

    e_max, tot = 0, 0
    while (e_max<len(nbs)):
        tot += nbs[e_max]
        if tot>nb_max:
            break
        e_max += 1

    # Compute the total number of possibilities by using between 0 and {e_nb} values from nbs.
    nb_possiblities = 0
    for i in range(max(0, e_min), min(len(nbs) + 1, e_max + 1)):
        nb_possiblities += compute((splits[0], ), nbs[:i]) * compute(splits[1:], nbs[i:])

    return nb_possiblities


nb = 0
for seq, nbs in rows:
    splits = get_splits(seq)
    s_nb = compute(splits, nbs)
    nb += s_nb
    print(s_nb)

print(nb)


###
# Part 2
###

nb = 0
for seq, nbs in rows:
    seq = '?'.join([seq] * 5)
    splits = get_splits(seq)
    nbs = nbs * 5
    s_nb = compute(splits, nbs)
    nb += s_nb
    print(s_nb)

print(nb)
