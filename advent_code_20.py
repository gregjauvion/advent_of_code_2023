
with open('input.txt', 'r') as f:
    d = [i.strip() for i in f.readlines()]

modules, vertices = {}, {}
for r in d:
    input, outputs = r.split(' -> ')
    outputs = outputs.split(', ')

    if '%' in input:
        modules[input[1:]] = {'type': 'flip-flop', 'state': False}
        vertices[input[1:]] = outputs
    elif '&' in input:
        modules[input[1:]] = {'type': 'conjunction', 'state': {}}
        vertices[input[1:]] = outputs
    elif input=='broadcaster':
        modules[input] = {'type': 'broadcaster'}
        vertices[input] = outputs

# Update state of conjunction modules
for i, j in vertices.items():
    for k in j:
        if (k in modules) and modules[k]['type']=='conjunction':
            modules[k]['state'][i] = '-'


def send_pulses(inputs):

    outputs = []
    for i, o, t in inputs:
        if o in modules:
            if modules[o]['type']=='flip-flop':
                if t=='-':
                    modules[o]['state'] = not modules[o]['state']
                    out_t = '+' if modules[o]['state'] else '-'
                    outputs.extend([(o, v, out_t) for v in vertices[o]])
            elif modules[o]['type']=='conjunction':
                modules[o]['state'][i] = t
                out_t = '-' if not '-' in modules[o]['state'].values() else '+'
                outputs.extend(([(o, v, out_t) for v in vertices[o]]))
            elif modules[o]['type']=='broadcaster':
                outputs.extend([(o, v, t) for v in vertices[o]])

    return outputs


nb_low, nb_high = 0, 0
for nb in range(1000):
    init = [(None, 'broadcaster', '-')]
    nb_low += 1
    outputs = init
    while len(outputs)>0:
        outputs = send_pulses(outputs)
        nb_low += len([t for i, o, t in outputs if t=='-'])
        nb_high += len([t for i, o, t in outputs if t == '+'])

print(nb_low, nb_high, nb_low * nb_high)