import re
import operator
from collections import defaultdict

with open('08_12_input.txt') as f:
    input_ = f.read()

examples = {"b inc 5 if a > 1\n\
a inc 1 if b < 5\n\
c dec -10 if a >= 1\n\
c inc -20 if c == 10": 10}


def str2intlst(str):
    return [int(i) for i in str if i]


str2op = {'inc': operator.add, 'dec': operator.sub,
          '>': operator.gt, '<': operator.lt,
          '>=': operator.ge, '<=': operator.le,
          '==': operator.eq, '!=': operator.ne}


def solver(str):
    register = defaultdict(lambda: 0)
    res = 0

    for line in str.split('\n'):
        line = line.strip()
        grps = re.match(r'(\w+) (\w+) (-?\d+) if (\w+) (\S+) (-?\d+)', line).groups()

        cond = str2op[grps[4]](register[grps[3]], int(grps[5]))
        if cond:
            register[grps[0]] = str2op[grps[1]](register[grps[0]], int(grps[2]))
            res = max(res, register[grps[0]])

    return res


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
