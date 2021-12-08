with open('06_12_input.txt') as f:
    input_ = f.read()

examples = {"0\t2\t7\t0": 5}
examples_steps = {"0\t2\t7\t0": [2, 4, 1, 2],
                  "2\t4\t1\t2": [3, 1, 2, 3],
                  "3\t1\t2\t3": [0, 2, 3, 4],
                  "0\t2\t3\t4": [1, 3, 4, 1],
                  "1\t3\t4\t1": [2, 4, 1, 2]}


def max_index(values):
    return max(range(len(values)), key=values.__getitem__)


class MemoryBank():
    def __init__(self, init_blocks):
        self.bank = init_blocks

    def redistribute(self):
        index = max_index(self.bank)
        value = self.bank[index]
        self.bank[index] = 0
        index = (index + 1) % len(self.bank)
        while value > 0:
            self.bank[index] += 1
            value -= 1
            index = (index + 1) % len(self.bank)

    def get_state(self):
        return hash(''.join([str(w)for w in self.bank]))


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    jump_list = str2intlst(str.split('\t'))
    bank = MemoryBank(jump_list)
    new_state = bank.get_state()
    states = []
    while new_state not in states:
        states.append(new_state)
        bank.redistribute()
        new_state = bank.get_state()
    return len(states)


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    def test(x):
        a = MemoryBank(str2intlst(x.split('\t')))
        a.redistribute()
        return a.bank
    test_all(examples_steps, test)
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
