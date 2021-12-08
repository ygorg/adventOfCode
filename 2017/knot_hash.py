import operator
from functools import reduce


def __get(lst, start=None, stop=None, step=None):
    if not start:
        start = 0
    if not stop:
        stop = len(lst)
    if not step:
        step = 1
    return [lst[i % len(lst)] for i in range(start, stop, step)]


def __set(lst, val, start=None, stop=None, step=None):
    if not start:
        start = 0
    if not stop:
        stop = len(lst)
    if not step:
        step = 1
    new_lst = [None for i in range(len(lst))]
    for i, i_lst in enumerate(range(start, stop, step)):
        new_lst[i_lst % len(lst)] = val[i]
    return [v if v is not None else lst[i % len(lst)] for i, v in enumerate(new_lst)]


def __debug_hash(hash_, index, knot_len):
    string = ['([{}]'.format(h) if i == index % len(hash_) else '{}'.format(h) for i, h in enumerate(hash_)]
    string[(index + knot_len - 1) % len(string)] += ')'
    print(' '.join(string))


def __sparse2dense(hash_, group=16):
    return [reduce(operator.xor, hash_[i:i + group], 0)
            for i in range(0, len(hash_), group)]


def __int2hex(lst):
    return [format(v, '02x') for v in lst]


def __round(hash_, knot_lenghts, nb=None):
    if nb is None:
        nb = 64

    index = 0
    skip_size = 0

    for _ in range(nb):
        for knot_len in knot_lenghts:
            reversed_knot = __get(hash_, index + knot_len - 1, index - 1, -1)
            hash_ = __set(hash_, reversed_knot, index, index + knot_len)
            index += knot_len + skip_size
            skip_size += 1

    return hash_


def sparse_knot_hash(str, hash_len=None, nb_round=None, pre_treat_str=None):
    if hash_len is None:
        hash_len = 256
    if pre_treat_str is None:
        pre_treat_str = lambda lst: [ord(c) for c in lst] + [17, 31, 73, 47, 23]

    hash_ = [i for i in range(hash_len)]
    knot_lengths = pre_treat_str(str)
    return __round(hash_, knot_lengths, nb=nb_round)


def knot_hash(str, hash_len=None, nb_round=None, pre_treat_str=None):
    sparse_hash = sparse_knot_hash(str, hash_len, nb_round, pre_treat_str)
    return ''.join(__int2hex(__sparse2dense(sparse_hash)))
