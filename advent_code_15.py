

def hash(s):

    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256

    return h


with open('input.txt', 'r') as f:
    d = f.read()


###
# Part 1
###

tot = 0
for s in d.split(','):
    tot += hash(s)

print(tot)


###
# Part 2
###

boxes = {i: [] for i in range(256)}
for s in d.split(','):
    if '=' in s:
        label, nb = s.split('=')
        nb = int(nb)
    else:
        label = s[:-1]

    ind = hash(label)
    e_label = [e for e in range(len(boxes[ind])) if boxes[ind][e][0] == label]

    if '-' in s:
        if len(e_label)==1:
            boxes[ind].pop(e_label[0])
    else:
        if len(e_label)==1:
            boxes[ind][e_label[0]] = (label, nb)
        else:
            boxes[ind].append((label, nb))

tot = 0
for i, b in boxes.items():
    tot += (i + 1) * sum([(e + 1) * i[1] for e, i in enumerate(b)])

print(tot)
