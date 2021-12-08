from collections import defaultdict

with open('13_12_input.txt') as f:
    input_ = f.read()

examples = {'0: 3\n\
1: 2\n\
4: 4\n\
6: 4': 24}


class Firewall(object):
    @staticmethod
    def time2index(t, r):
        """Convert time into scanner index

        :param t: Actual time
        :type t: int
        :param r: Range of the firewall
        :type r: int
        :returns: Index of the scanner
        :rtype: {int}
        """
        r -= 1
        return r - abs((t % (r * 2)) - r)

    def __init__(self, init):
        # range of the firewalls, and actual index of scanner
        self.layers = defaultdict(lambda: (0, -1))
        for depth, range_ in init:
            self.layers[depth] = range_, 0
        # Max depth
        self.nb_scanner = max(self.layers.keys()) + 1
        self.max_range = max([r for r, _ in self.layers.values()])
        self.time = 1
        # Layer in which the packet is
        self.packet_index = -1

    def forward_rider(self):
        """Compute severity at a given time

        [description]
        :returns: Severity at time `self.time`
        :rtype: {int}
        """
        self.packet_index += 1
        current_layer = self.layers[self.packet_index]
        print('Rider: {}, scanner: {}, range: {}'.format(self.packet_index, current_layer[1], current_layer[0]))
        if current_layer[1] == 0 and current_layer[0] > 0:
            print('Caught !')
            return self.packet_index * current_layer[0]
        return 0

    def update(self):
        """Increment time and update scanner indexes
        """
        self.layers = {depth: (range_, Firewall.time2index(self.time, range_))
                       if range_ > 0 else (0, 0)
                       for depth, (range_, index) in self.layers.items()}
        self.time += 1

    def print_node(self, i, r):
        """Return repr of the node of the `i`th layer and `r`th depth

        The firewalls are a matrix (self.nb_scanner, self.max_range)
        :param i: layer index
        :type i: int
        :param r: depth index
        :type r: int
        :returns: Representation of the node
        :rtype: {str}
        """
        if i == self.packet_index and r == 0:
            out = '({})'
        elif r < self.layers[i][0]:
            out = '[{}]'
        elif r == 0:
            out = '.{}.'
        else:
            out = '   '
        if r == self.layers[i][1] and self.layers[i][0] > 0:
            out = out.format('S')
        elif r == 0 and self.layers[i][0] == 0:
            out = out.format('.')
        else:
            out = out.format(' ')
        return out

    def print(self):
        print('Picosecond {}:'.format(self.time))
        strlst = [' {} '.format(i) for i in range(self.nb_scanner)]
        print(' '.join(strlst))
        for r in range(self.max_range):
            strlst = [self.print_node(i, r) for i in range(self.nb_scanner)]
            print(' '.join(strlst))
        print()


def str2intlst(str):
    return [int(i) for i in str if i]


def time2index(t, r):
    """ Compute the index of the scanner given the time and the range
    """
    r -= 1
    return r - abs((t % (r * 2)) - r)


def severity(init, delay=0):
    """ Compute the severity of the journey accross the firewalls
        after a given delay
    """
    return sum(d * r for d, r in init
               if time2index(d + delay, r) == 0)


def solver(str):
    data = [str2intlst(line.split(': ')) for line in str.split('\n')]
    f = Firewall(data)
    print('Initial State')
    f.print()
    severity = 0
    for i in range(f.nb_scanner):
        severity += f.forward_rider()
        # f.print()
        f.update()
        # f.print()
    return severity


def solver(str):
    data = [str2intlst(line.split(': ')) for line in str.split('\n')]
    return simple_severity(data)


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
