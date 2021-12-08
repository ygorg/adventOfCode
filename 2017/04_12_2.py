from collections import Counter

with open('04_12_input.txt') as f:
    input_ = f.read()

examples = {"abcde fghij": 1, "abcde xyz ecdab": 0,
            "a ab abc abd abf abj": 1, "iiii oiii ooii oooi oooo": 1,
            "oiii ioii iioi iiio": 0}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    passphrases = [line.split(' ') for line in str.split('\n')]
    valid_passphrases = 0
    for passphrase in passphrases:
        count_words = []
        for w in passphrase:
            count = Counter(w)
            keys = sorted(count.keys())
            count_words.append(''.join(['{}{}'.format(k, count[k]) for k in keys]))
        count_words = Counter(count_words)
        print(count_words)
        repeatable_words = sum([1 if c > 1 else 0 for c in count_words.values()])
        if repeatable_words == 0:
            valid_passphrases += 1

    return valid_passphrases


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example, res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
