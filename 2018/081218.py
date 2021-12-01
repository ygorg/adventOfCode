import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2': 138
        }

    def read_node(self, input, depth=0):
        logging.debug('input : {}'.format(input))
        nb_child = input.pop(0)
        nb_meta = input.pop(0)
        logging.debug('Childs : {} Meta : {}'.format(nb_child, nb_meta))
        logging.debug('input : {}'.format(input))
        res = 0
        for i in range(nb_child):
            logging.debug('Visiting child')
            res += self.read_node(input, depth=depth + 1)
        logging.debug('No more child')
        logging.debug('Metadata')
        for _ in range(nb_meta):
            res += input.pop(0)
        return res

    def _solve(self, input):
        input = list(map(int, input.split(' ')))
        return self.read_node(input)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2': 66
        }

    def read_node(self, input, depth=0):
        logging.debug('Child at {}'.format(depth))
        nb_child = input.pop(0)
        nb_meta = input.pop(0)
        logging.debug('Childs : {} Meta : {}'.format(nb_child, nb_meta))
        children_val = []
        res = 0
        for i in range(nb_child):
            children_val.append(self.read_node(input, depth=depth + 1))
        logging.debug('Metadata at {}'.format(depth))
        if nb_child == 0:
            logging.debug('No child, summing')
        else:
            logging.debug('Getting child values')
        for _ in range(nb_meta):
            value = input.pop(0)
            logging.debug('Metadata : {}'.format(value))
            if nb_child == 0:
                res += value
            else:
                index = value - 1
                logging.debug('Child {}'.format(index))
                if index < nb_child:
                    res += children_val[index]
        logging.debug('Node value : {}'.format(res))
        return res


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
