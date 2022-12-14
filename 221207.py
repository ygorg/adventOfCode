import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n5626152 d.ext\n7214296 k': 95437
        }

    def pre_treat(self, inp_):
        return [l.strip().split(' ')
                for l in inp_.split('\n') if l]

    def read(self, output):
        sizes = 0
        while output and output[0][0] != '$':
            instr = output.pop(0)
            if instr[0] != 'dir':
                sizes += int(instr[0])
        return output, sizes

    def through(self, output):
        cum_size = 0
        filt_size = 0
        while output:
            instr = output.pop(0)
            if instr.pop(0) != '$':
                print('Error')
            if instr[0] == 'cd':
                if instr[1] == '..':
                    if cum_size < 100000:
                        filt_size += cum_size
                    return output, cum_size, filt_size
                else:
                    output, below_size_, filt_size_ = self.through(output)
                    filt_size += filt_size_
                    # print(f'Taille de {instr[1]}: {below_size_}')
                    cum_size += below_size_
            elif instr[0] == 'ls':
                output, file_sizes = self.read(output)
                # tree.append(files)
                cum_size += file_sizes
        if cum_size < 100000:
            filt_size += cum_size
        return output, cum_size, filt_size

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        _, _, res = self.through(inp_)
        return res


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n5626152 d.ext\n7214296 k': 24933642
        }

    def through(self, output, d='/'):
        cum_size = 0
        dir_sizes = {}
        # while theres instructions
        while output:
            instr = output.pop(0)
            if instr.pop(0) != '$':
                # If there's no $ then we should be reading `ls` output
                print('Error')
            if instr[0] == 'cd':
                if instr[1] == '..':
                    # End the recursion, quit the directory
                    dir_sizes[d] = cum_size
                    return output, cum_size, dir_sizes
                else:
                    output, below_size_, dir_sizes_ = self.through(output, instr[1])
                    dir_sizes.update(dir_sizes_)
                    cum_size += below_size_
            elif instr[0] == 'ls':
                output, file_sizes = self.read(output)
                cum_size += file_sizes
        dir_sizes[d] = cum_size
        return output, cum_size, dir_sizes

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        _, _, dir_sizes = self.through(inp_)
        # Doesn't need the dict but it prints better
        free_space = 70000000 - dir_sizes['/']
        min_free = 30000000 - free_space
        dir_sizes = {k: v for k, v in dir_sizes.items() if v > min_free}
        return min(dir_sizes.values())


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
