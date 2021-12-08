from collections import Counter

with open('05_12_input.txt') as f:
    input_ = f.read()

examples = {"0\n3\n0\n1\n-3": 10}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    jump_list = str2intlst(str.split('\n'))
    current_index = 0
    count_jump = 0
    while current_index in range(len(jump_list)):
        # print(jump_list, current_index, jump_list[current_index])
        saved_index = current_index
        current_index += jump_list[current_index]
        if jump_list[saved_index] >= 3:
            jump_list[saved_index] -= 1
        else:
            jump_list[saved_index] += 1
        count_jump += 1
    return count_jump


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
