knot_hash = __import__('10_12_2')
knot_hash = knot_hash.knot_hash

with open('14_12_input.txt') as f:
    input_ = f.read()

examples = {'flqrgnkx': 1242}
# examples_min = {'flqrgnkx': '11.2.3..\n.1.2.3.4\n....5.6.\n7.8.55.9\n.88.5...\n88..5..8\n.8...8..\n88.8.88.'}
examples_min = {'11\n11': 1,
                '00\n00': 0,
                '10': 1,
                '1': 1,
                '0': 0,
                '101\n010\n101': 5,
                '11101\n00011\n11010\n01011\n01101\n00111': 2}


def str2intlst(str):
    return [int(i) for i in str if i]


def hex2bin(hex):
    return bin(int(hex, 16))[2:].zfill((len(hex)) * 4)


def disk_map(str):
    for i in range(128):
        print(i)
        seed = '{}-{}'.format(str, i)
        hash_ = knot_hash(seed)
        yield str2intlst(hex2bin(hash_))


def get(iterable):
    for i in iterable:
        return i


def connex_composants(iterable):
    ind2reg = {}
    reg2ind = {}

    # print(iterable)

    for i, line in enumerate(iterable):
        # print(iterable[i - 1]) if i != 0 else print([0 for k in range(len(line))])
        # print(iterable[i])
        for j in range(len(line)):
            if line[j] == 0:
                continue
            index = i * len(line) + j
            # retrouver le fichier ou je génère tout les voisoins
            # faire une liste avec tout les voisins et leur region
            # si plusieurs région on garde le fait que la region x == la région y

            ind2reg[index] = index
            if index not in reg2ind:
                reg2ind[index] = []
            reg2ind[index].append(index)

            # print('\t', index)
            # print(reg2ind)

            region_to_merge = {index}

            neighb = []
            if i != 0:
                neighb.append(index - len(line))
            if j != 0:
                neighb.append(index - 1)

            for n in neighb:
                if n in ind2reg:
                    region_to_merge |= set([ind2reg[n]])

            new_index = region_to_merge.pop()

            # print('Merging {} with {}'.format(new_index, region_to_merge))

            for merge_index in region_to_merge:
                reg2ind[new_index] += reg2ind[merge_index]
                for jko in reg2ind[merge_index]:
                    ind2reg[jko] = new_index
                del reg2ind[merge_index]

            # print(reg2ind)
            # print()

    return len(reg2ind)


def solver(str):
    # regions : list of list of nodes
    # regions : dict node->group
    return connex_composants(disk_map(str))


def solver_min(str):
    disk_m = [str2intlst(l) for l in str.split('\n')]
    return connex_composants(disk_m)


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all(examples_min, solver_min)
    # test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
