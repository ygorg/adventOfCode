import logging
from base import Base
from binarytree import Node, _build_tree_string
from itertools import permutations
import json
from tqdm import tqdm

NODE = -1


# Printing trees with depth
def tmp(self) -> str:
    lines = _build_tree_string(self, 0, False, "-")[0]
    return "\n".join(((f'{i//2:2d} ' if (i + 1) % 2 else '   ') + line.rstrip() for i, line in enumerate(lines)))


Node.__str__ = tmp


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '[1,1]\n[2,2]\n[3,3]\n[4,4]': 445,
            '[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]': 19,
            '[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]': 27,
            '[7,7]\n[8,8]\n[9,9]\n[4,4]\n[5,5]\n[6,6]': 27,
            '[[[[4,3],4],4],[7,[[8,4],9]]]\n[1,1]': 2,
            '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]\n[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]\n[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]\n[7,[5,[[3,8],[1,4]]]]\n[[2,[2,2]],[8,[8,1]]]\n[2,9]\n[1,[[[9,3],9],[[9,0],[0,7]]]]\n[[[5,[7,4]],7],1]\n[[[[4,2],2],6],[8,7]]': 38,
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n[[[5,[2,8]],4],[5,[[9,9],0]]]\n[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n[[[[5,4],[7,7]],8],[[8,3],8]]\n[[9,3],[[9,9],[6,[4,9]]]]\n[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]': 4140,
        }

    def list2tree(self, val):
        if isinstance(val, int):
            return Node(val)
        else:
            a, b = val
            return Node(NODE, self.list2tree(a), self.list2tree(b))

    def magnitude(self, tree):
        if tree.val == NODE:
            return (self.magnitude(tree.left) * 3
                    + self.magnitude(tree.right) * 2)
        else:
            return tree.val

    def explode(self, tree, root=None, d=0):
        if root is None:
            root = tree
        if tree.val == NODE:
            if d >= 4 and tree.left.value != NODE and tree.right.value != NODE:
                # too deep and two leafs
                lst = root.inorder
                idx = lst.index(tree)

                # finding left neighbor
                i = idx - 2
                while i >= 0 and lst[i].val == NODE:
                    i -= 1
                if i >= 0:
                    lst[i].value += tree.left.value

                # finding right neighbor
                i = idx + 2
                while i < len(lst) and lst[i].val == NODE:
                    i += 1
                if i < len(lst):
                    lst[i].value += tree.right.value

                logging.debug(f"Exploding {tree.left.val}/ \\{tree.right.val}")

                tree.right = None
                tree.left = None
                tree.value = 0
                return True
            else:
                return self.explode(tree.left, root, d + 1) or self.explode(tree.right, root, d + 1)
        else:
            return False

    def split(self, tree):
        if tree.val != NODE:
            # in leaf
            if tree.val >= 10:
                logging.debug(f"Splitting {tree.val}")
                tree.left = Node(tree.val // 2)
                tree.right = Node(tree.val // 2 + tree.val % 2)
                tree.val = NODE
                return True
            else:
                return False
        else:
            return self.split(tree.left) or self.split(tree.right)

    def reduce(self, tree):
        need_explosion = tree.height > 4
        need_split = any(v.val >= 10 for v in tree.leaves)
        while need_explosion or need_split:
            if need_explosion:
                self.explode(tree)
            else:
                self.split(tree)
            #input(tree)
            need_explosion = tree.height > 4
            need_split = any(v.val >= 10 for v in tree.leaves)

    def add(self, a, b):
        return Node(NODE, a, b)

    def pre_treat(self, inp_):
        return [json.loads(l)
                for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        acc = inp_.pop(0)
        acc = self.list2tree(acc)
        for t in inp_:
            t = self.list2tree(t)
            acc = self.add(acc, t)
            #input(acc)
            logging.debug("Add new tree")
            self.reduce(acc)
        return self.magnitude(acc)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n[[[5,[2,8]],4],[5,[[9,9],0]]]\n[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n[[[[5,4],[7,7]],8],[[8,3],8]]\n[[9,3],[[9,9],[6,[4,9]]]]\n[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]': 3993,
        }

    def _solve(self, inp_):
        """Brute forcing, i don't know how to optimze that...
        but it only takes 40s so ¯\_(ツ)_/¯"""
        inp_ = self.pre_treat(inp_)
        magnitudes = {}
        m = -1
        for i, j in tqdm(permutations(range(len(inp_)), 2)):
            if (i, j) in magnitudes:
                continue
            a, b = self.list2tree(inp_[i]), self.list2tree(inp_[j])
            res = self.add(a, b)
            #input(res)
            self.reduce(res)
            magnitudes[(i, j)] = self.magnitude(res)
            if magnitudes[(i, j)] > m:
                m = magnitudes[(i, j)]
                print("max: ", m)
        return max(magnitudes.values())


if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            '-t', '--test', action='store_true', help='Execute tests')
        parser.add_argument(
            '-s', '--second', action='store_true', help='Execute second')
        parser.add_argument(
            '-d', '--debug', action='store_true', help='Print debug info')
        args = parser.parse_args()
        return args

    args = arguments()

    if args.second:
        solver = Second(args.test)
    else:
        solver = First(args.test)
    if args.test:
        logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
        solver.solve()
