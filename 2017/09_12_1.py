with open('09_12_input.txt') as f:
    input_ = f.read()

examples = {'{}': 1,
            '{{{}}}': 6,
            '{{},{}}': 5,
            '{{{},{},{{}}}}': 16,
            '{<a>,<a>,<a>,<a>}': 1,
            '{{<ab>},{<ab>},{<ab>},{<ab>}}': 9,
            '{{<!!>},{<!!>},{<!!>},{<!!>}}': 9,
            '{{<a!>},{<a!>},{<a!>},{<ab>}}': 3}


def str2intlst(str):
    return [int(i) for i in str if i]


def fst(string):
    try:
        return string[0]
    except IndexError:
        return ''


def snd(string):
    return string[1:]


def split(string):
    return fst(string), snd(string)


def GR(string, args):
    s, tring = split(string)
    if s != '{':
        raise AttributeError('GR : {}'.format(s))
    args = args['func'](s, args)

    string, args = LS(tring, args)

    s, tring = split(string)
    if s != '}':
        raise AttributeError('GR : {}'.format(s))
    args = args['func'](s, args)

    string = tring
    return string, args


def GA(string, args):
    s, tring = split(string)
    if s != '<':
        raise AttributeError('GA : {}'.format(s))
    args = args['func'](s, args)
    string = tring

    acc = ''
    s, string = split(string)
    while s != '>':
        acc += s
        if s == '!':
            s, string = split(string)
            acc += s
        s, string = split(string)
    args = args['func'](acc, args)

    if s != '>':
        raise AttributeError('GA : {}'.format(s))
    args = args['func'](s, args)
    return string, args


def S(string, args):
    s = fst(string)
    if s == '{':
        string, args = GR(string, args)
    elif s == '<':
        string, args = GA(string, args)
    elif s == '}':
        ()
    else:
        print(string)
        raise AttributeError('S : {}'.format(s))
    return string, args


def LS(string, args):
    string, args = S(string, args)

    s, tring = split(string)
    if s == ',':
        args = args['func'](s, args)
        string, args = LS(tring, args)
    return string, args


def f(c, args):
    if c == '<':
        args['in_ga'] = True
    elif c == '>':
        args['in_ga'] = False

    if c == '}' and not args['in_ga']:
        args['depth'] -= 1
    # print_score = str(args['depth']) if c == '}' else ''
    # print('{}{} {}'.format('\t' * args['depth'], c, print_score))
    if c == '{' and not args['in_ga']:
        args['depth'] += 1
        args['score'] += args['depth']

    return args


def solver(str):
    string, args = LS(str, {'func': f, 'depth': 0, 'score': 0, 'in_ga': False})
    return args['score']


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
