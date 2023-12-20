import numpy as np

with open('input.txt', 'r') as f:
    d1, d2 = f.read().split('\n\n')


def read_comparison(c):
    """ Reads a comparison like 'x<10' and returns the corresponding lambda function
    which inputs a dict with the values of the variables.
    """

    if '<' in c:
        variable, value = c.split('<')
        return lambda values: values[variable] < int(value)
    elif '>' in c:
        variable, value = c.split('>')
        return lambda values: values[variable] > int(value)

def parse_condition(conditions):
    """ Reads a condition formed with {comparison}:{c_true},{c_false}
    and build the corresponding lambda function which inputs values, workflows.
    """

    c = read_comparison(conditions.split(':', 1)[0])
    c_true, c_false = conditions.split(':', 1)[1].split(',', 1)

    def read_result(r):
        """ Function used to read {c_true} and {c_false}.
        Returns a lambda function which inputs values, workflows
        """
        if r=='A':
            return lambda values, workflows: True
        elif r=='R':
            return lambda values, workflows: False
        elif ('<' in r) or ('>' in r):
            return parse_condition(r)
        else:
            return lambda values, workflows: workflows[r](values, workflows)

    return lambda values, workflows: read_result(c_true) if c(values) else read_result(c_false)

def evaluate(f, v, workflows):

    res = f(v, workflows)
    if type(res)==bool:
        return res
    else:
        return evaluate(res, v, workflows)

# Parse the variables as a dict
v_values = []
for v in d2.split('\n'):
    vv = {}
    for i, j in [i.split('=') for i in v[1:-1].split(',')]:
        vv[i] = int(j)

    v_values.append(vv)

# Parse the workflows as a list of conditions to evaluate
workflows = {}
for w in d1.split('\n'):
    name, conditions = w.split('{')
    conditions = conditions[:-1]

    workflows[name] = parse_condition(conditions)


###
# Part 1
###

tot = 0
for v in v_values:
    if evaluate(workflows['in'], v, workflows):
        tot += sum(v.values())

print(tot)


###
# Part 2
###

b_min, b_max = 1, 4000

workflows = {}
for w in d1.split('\n'):
    name, conditions = w.split('{')
    conditions = conditions[:-1]
    workflows[name] = conditions

def get_area(bounds, condition):

    if condition=='A':
        return np.prod([j - i + 1 for i, j in bounds.values()])
    elif condition=='R':
        return 0
    elif ('<' in condition) or ('>' in condition):
        comparison = condition.split(':', 1)[0]

        # Manage both cases
        if '<' in comparison:
            variable, value = comparison.split('<')
            value = int(value)
            c_true, c_false = condition.split(':', 1)[1].split(',', 1)
        if '>' in comparison:
            variable, value = comparison.split('>')
            value = int(value)
            value += 1
            c_false, c_true = condition.split(':', 1)[1].split(',', 1)

        # Split the problem
        min_, max_ = bounds[variable]
        if value <= min_:
            return get_area(bounds, c_false)
        elif min_ < value <= max_:
            b_inf = {v: b if v!=variable else [b[0], value - 1] for v, b in bounds.items()}
            b_sup = {v: b if v != variable else [value, b[1]] for v, b in bounds.items()}
            return get_area(b_inf, c_true) + get_area(b_sup, c_false)
        else:
            return get_area(bounds, c_true)

    else:
        return get_area(bounds, workflows[condition])

init_bounds = {c: [b_min, b_max] for c in 'maxs'}
print(get_area(init_bounds, workflows['in']))
