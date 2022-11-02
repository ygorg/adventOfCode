import logging
from base import Base
from math import prod
import logging

logging.basicConfig(level=logging.WARNING)
""" Bit to hex
a = ""
''.join([hex(int(''.join(e), 2))[-1].upper() for e in list(grouper(a, 4))])
"""

def gt(it):
    return int(it[0] > it[1])
def lt(it):
    return int(it[0] < it[1])
def eq(it):
    return int(it[0] == it[1])

op = {0: sum, 1: prod, 2: min, 3: max, 5: gt, 6: lt, 7: eq}

def eat(data, n):
    return data[n:], data[:n]

def eati(data, n):
    return data[n:], int(data[:n], 2)


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'D2FE28': 6,
            '38006F45291200': 9,
            'EE00D40C823060': 14,
            '8A004A801A8002F478': 16,
            '620080001611562C8802118E34': 12,
            'C0015000016115A2E0802F182340': 23,
            'A0016C880162017C3686B18A3D4780': 31
        }

    def pre_treat(self, inp_):
        return ''.join(format(int(c, 16), '0>4b') for c in inp_.strip())

    def parse_num(self, data):
        logging.debug('parsing num: {}'.format(data[::-1]))
        acc = ""
        while data[0] == "1":
            data, tmp = eat(data, 5)
            acc += tmp[1:]
        data, tmp = eat(data, 5)
        acc += tmp[1:]
        n = int(acc, 2)
        logging.debug('parsed  num: {} {}'.format(data[::-1], n))
        return data, n

    def parse_op(self, data):
        logging.debug('parsing op : {}'.format(data[::-1]))
        data, lgh = eat(data, 1)
        logging.debug('parsing    : {} {}'.format(data[::-1], lgh))
        n = 0
        if lgh == "0":
            data, pkt_len = eati(data, 15)
            logging.debug('parsing    : {} {}'.format(data[::-1], pkt_len))
            data, sub_pkt = eat(data, pkt_len)
            while sub_pkt:
                sub_pkt, val = self.parse_packet(sub_pkt)
                n += val
        else:
            data, pkt_nb = eati(data, 11)
            logging.debug('parsing    : {} {}'.format(data[::-1], pkt_nb))
            for _ in range(pkt_nb):
                data, val = self.parse_packet(data)
                n += val
        logging.debug('parsed  op : {} {}'.format(data[::-1], n))
        return data, n

    def parse_packet(self, data):
        logging.debug('parsing pkt: {}'.format(data[::-1]))
        data, ver = eati(data, 3)
        data, pkt = eati(data, 3)
        logging.debug('parsing    : {} {} {}'.format(data[::-1], ver, pkt))
        if pkt == 4:  # number
            data, n = self.parse_num(data)
            n = 0
        else:  # operator
            data, n = self.parse_op(data)
        logging.debug('parsed  pkt: {} {}'.format(data[::-1], n))
        return data, ver + n

    def _solve(self, inp_):
        data = self.pre_treat(inp_)
        data, n = self.parse_packet(data)
        return n


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'C200B40A82': 3,
            '04005AC33890': 54,
            '880086C3E88112': 7,
            'CE00C43D881120': 9,
            'D8005AC2A8F0': 1,
            'F600BC2D8F': 0,
            '9C005AC2F8F0': 0,
            '9C0141080250320F1802104A08': 1
        }

    def parse_op(self, data, op):
        logging.debug('parsing op : ', data[::-1])
        data, lgh = eat(data, 1)
        logging.debug('parsing    : ', data[::-1], lgh)
        val = []
        if lgh == "0":
            data, pkt_len = eati(data, 15)
            logging.debug('parsing    : ', data[::-1], pkt_len)
            data, sub_pkt = eat(data, pkt_len)
            while sub_pkt:
                sub_pkt, n = self.parse_packet(sub_pkt)
                val.append(n)
        else:
            data, pkt_nb = eati(data, 11)
            logging.debug('parsing    : ', data[::-1], pkt_nb)
            for _ in range(pkt_nb):
                data, n = self.parse_packet(data)
                val.append(n)
        n = op(val)
        logging.debug('parsed  op : ', data[::-1], n, op.__name__, val)
        return data, n

    def parse_packet(self, data):
        logging.debug('parsing pkt: ', data[::-1])
        data, ver = eati(data, 3)
        data, pkt = eati(data, 3)
        logging.debug('parsing    : ', data[::-1], ver, pkt)
        if pkt == 4:  # number
            data, n = self.parse_num(data)
        else:  # operator
            data, n = self.parse_op(data, op[pkt])
        logging.debug('parsed  pkt: ', data[::-1], n)
        return data, n


if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            '-t', '--test', action='store_true', help='Execute tests')
        parser.add_argument(
            '-s', '--second', action='store_true', help='Execute second')
        args = parser.parse_args()
        return args

    args = arguments()

    if args.second:
        solver = Second(args.test)
    else:
        solver = First(args.test)
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.INFO)
        solver.solve()
