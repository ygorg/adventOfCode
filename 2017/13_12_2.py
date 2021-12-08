with open('13_12_input.txt') as f:
    input_ = f.read()

examples = {'0: 3\n\
1: 2\n\
4: 4\n\
6: 4': 10,
            '0: 2\n\
1: 2': None}


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


def can_cross(init, delay=0):
    """ Tell whether the package will safely cross the firewalls
        after a given delay
    """
    return sum(1 for d, r in init
               if time2index(d + delay, r) == 0) == 0


def range_index(init, delay=0):
    """ Returns the position of each scanner for a given delay
    """
    return [time2index(d + delay, r) for d, r in init]


def ppcm(*n):
    def _pgcd(a, b):
        while b:
            a, b = b, a % b
        return a
    p = abs(n[0] * n[1]) // _pgcd(n[0], n[1])
    for x in n[2:]:
        p = abs(p * x) // _pgcd(p, x)
    return p


def gen(data):
    x = {}
    for d, r in data:
        tmp = 2 * r - 2
        if tmp not in x:
            x[tmp] = []
        x[tmp].append((tmp - d) % tmp)

    if len(x) != 1:
        period = ppcm(*x.keys())
    else:
        for i in x.keys():
            period = i
            break

    # Sorting so the lower modulo will be checked first
    # (for example %2 will be checked first)
    rules = [(k, x[k]) for k in sorted(x.keys())]

    def ok(delay):
        """Check if `delay` respects all rules
        """
        for m, p in rules:
            if (i % m) in p:
                return False
        return True

    for i in range(period):
        if ok(i):
            yield i
    yield None


def solver(str):
    """Solve the given problem

    The idea here is to filter delays values that cannot work based on the fact
    that at a given delay one firewall scanner will be catch the package
    This method ensures that the program will end even if the puzzple has no
    answer ("0: 2\n1: 2" has no answer)

    :param str: The puzzle input
    :type str: [str]
    :returns: Delay where the package will not get caught
    :rtype: {int}
    """
    # Pre-treat the input
    data = [str2intlst(line.split(': ')) for line in str.split('\n')]

    # `gen` returns delays where the package will not get caught
    return next(gen(data))


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
