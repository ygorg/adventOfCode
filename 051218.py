from base import Base
import logging


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            'aA': 0,
            'abBA': 0,
            'abAB': 4,
            'aabAAB': 6,
            'dabAcCaCBAcCcaDA': 10
        }

    def react(self, a, b):
        return a.lower() == b.lower() and a != b

    def _solve(self, input):
        stack = list()
        for unit in input:
            stack.append(unit)
            logging.debug(''.join(stack))
            if len(stack) < 2:
                continue
            if self.react(stack[-1], stack[-2]):
                stack.pop()
                stack.pop()
                logging.debug(''.join(stack) + ' Reaction !')
        return len(stack)


class Second(First):
    def __init__(self):
        super(Second, self).__init__()
        self.examples = {
            'dabAcCaCBAcCcaDA': 4
        }

    def _solve(self, input):
        min_unit = len(input)
        for unit_type in set(input.lower()):
            logging.info('Removing {}'.format(unit_type))
            stack = list()
            for unit in input:
                if unit.lower() == unit_type:
                    continue
                stack.append(unit)
                logging.debug(''.join(stack))
                if len(stack) < 2:
                    continue
                if self.react(stack[-1], stack[-2]):
                    stack.pop()
                    stack.pop()
                    logging.debug(''.join(stack) + ' Reaction !')
            logging.info('Removing {} is {}'.format(unit_type, len(stack)))
            if len(stack) < min_unit:
                min_unit = len(stack)
        return min_unit


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
        solver = Second()
    else:
        solver = First()
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.INFO)
        solver.solve()
