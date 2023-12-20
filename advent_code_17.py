import numpy as np

with open('input_test.txt', 'r') as f:
    data = np.array([list(i.strip()) for i in f.readlines()], dtype=int)



# A state is formed the following way: (loss, x, y, up_speed, down_speed, left_speed, right_speed)
losses = []
max_speed = 3
states = [(0, 0, 0, 0, 0, 0, 0)]
history = {}
while len(states)>0:
    state = states.pop()
    if state[1:] in history:# and history[state[1:]]<=state[0]:
        continue

    history[state[1:]] = state[0]

    # Generate the new states
    loss, x, y, up_s, down_s, left_s, right_s = state
    if x==data.shape[0]-1 and y==data.shape[1]-1:
        losses.append(loss)
        continue

    if up_s<max_speed and x>0 and down_s==0:
        states.append((loss + data[x - 1, y], x - 1, y, up_s + 1, 0, 0, 0))
    if down_s<max_speed and x<data.shape[0]-1 and up_s==0:
        states.append((loss + data[x + 1, y], x + 1, y, 0, down_s + 1, 0, 0))
    if left_s<max_speed and y>0 and right_s==0:
        states.append((loss + data[x, y - 1], x, y - 1, 0, 0, left_s + 1, 0))
    if right_s<max_speed and y<data.shape[1] - 1 and left_s==0:
        states.append((loss + data[x, y + 1], x, y + 1, 0, 0, 0, right_s + 1))

print(min(losses))
