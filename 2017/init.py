#! /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import argparse


def arguments():
    parser = argparse.ArgumentParser(description="Script desc")
    parser.add_argument('DAY', type=int,
                        help='Day of the calendar')
    args = parser.parse_args()
    return args


args = arguments()
day = args.DAY

files = ['{}_12_1.py', '{}_12_2.py', '{}_12_input.txt']

files = [f.format(day) for f in files]

content = "with open('" + files[-1] + "') as f:\n\
    input_ = f.read()\n\
examples = {'': None}\n\
\n\n\
def str2intlst(str):\n\
    return [int(i) for i in str if i]\n\
\n\n\
def solver(str):\n\
    return None\n\
\n\n\
def test_all(examples, fct, fct_param=None):\n\
    if fct_param is None:\n\
        fct_param = {}\n\
    valid_example = 0\n\
    for example, solution in examples.items():\n\
        res = fct(example, **fct_param)\n\
        valid_example += 1 if res == solution else 0\n\
        print('{} -> {} : {} {}'.format(example.replace('\\n', '\\\\n'), res, solution, 'O' if res == solution else 'X'))\n\
\n\
    print('{}/{} good answer'.format(valid_example, len(examples)))\n\
\n\n\
if __name__ == '__main__':\n\
    test_all(examples, solver)\n\
    print('Input answer : {}'.format(solver(input_)))\n\
"

for file_name in files:
    with open(file_name, 'w') as file:
        if '.py' in file_name:
            file.write(content)
