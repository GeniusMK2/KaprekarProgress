# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import signal
import sys
from random import randint

import numpy.random
from pandas import DataFrame, concat
from tqdm import tqdm

result = DataFrame(
    columns=["numeration_base", "digit", "number", "repeat_sequence", "repeat_sequence_length", "steps"]
)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def separate_number(number, digit, numeration_base=10):
    ret = []
    while number >= numeration_base:
        ret.append(math.floor(number % numeration_base))
        number = math.floor(number / numeration_base)
    ret.append(number)
    while len(ret) < digit + 1:
        ret.append(0)
    ret.reverse()
    return ret


def concat_number(list_num, numeration_base=10):
    ret = 0
    for power in range(len(list_num)):
        ret += list_num[-power - 1] * pow(numeration_base, power)
    return ret


def kaprekar_algorithm_once(number, digit, numeration_base):
    max_num = concat_number(sorted(separate_number(number, digit, numeration_base), reverse=True), numeration_base)
    min_num = concat_number(sorted(separate_number(number, digit, numeration_base), reverse=False), numeration_base)
    return max_num - min_num


def recurrence_kaprekar_algorithm(number, digit, numeration_base):
    tmp_nums = []
    while number not in tmp_nums:
        tmp_nums.append(number)
        number = kaprekar_algorithm_once(number, digit, numeration_base)
    return tmp_nums[tmp_nums.index(number):], len(tmp_nums) - 1


def check_range(digit, numeration_base):
    """
    Give digit and numeration_base, check every number in that range whether satisfy Kaprekar conjecture.
    :param digit:
    :param numeration_base:
    :return:
    """

    global result
    for num in range(pow(numeration_base, digit), pow(numeration_base, digit + 1)):
        seq, steps = recurrence_kaprekar_algorithm(num, digit, numeration_base)

        print("Base:{},Digit:{},Number:{},Rep_Seq:{},Len:{},Step:{}".format(
            numeration_base, digit + 1,  # 位数为科学计数法计数+1
            num, str(seq), len(seq), steps
        ))
        result = concat([result,
                         DataFrame({
                             "numeration_base": numeration_base,
                             "digit": digit + 1,  # 位数为科学计数法计数+1
                             "number": num,
                             "repeat_sequence": str(seq),
                             "repeat_sequence_length": len(seq),
                             "steps": steps
                         }, index=[""])])


def check_random(digit, numeration_base):
    pass


def build_random(digit, numeration_base):
    return randint(numeration_base ** digit, numeration_base ** (digit+1) - 1)


def total():
    global result
    for _n in range(1, 100):
        _numeration_base = _n * 2
        for _digit in range(2, 3):
            print("{}进制{}位数:".format(_numeration_base, _digit+1))
            check_range(_digit, _numeration_base)
    result.to_csv("./结果.csv")
    # result = result.drop(index=result.index)


def func(x):
    return 0.5 * x ** 3 - 0.5 * x


def total2():
    global result
    for _n in range(1, 1000):
        _numeration_base = _n * 2
        _digit = 2
        num = build_random(_digit, _numeration_base)
        # print("{}进制{}位数:{}".format(_numeration_base, _digit+1, num))
        seq, steps = recurrence_kaprekar_algorithm(num, _digit, _numeration_base)
        print("Base:{},Digit:{},Number:{},Rep_Seq:{},Len:{},Step:{}".format(
            _numeration_base, _digit + 1,  # 位数为科学计数法计数+1
            num, str(seq), len(seq), steps
        ))
        print(func(_numeration_base)-seq[0])
        result = concat([result,
                         DataFrame({
                             "numeration_base": _numeration_base,
                             "digit": _digit + 1,  # 位数为科学计数法计数+1
                             "number": num,
                             "repeat_sequence": seq[0],
                             "repeat_sequence_length": len(seq),
                             "steps": steps
                         }, index=[""])])

    result.to_csv("./结果.csv")


def caught_signal(_, __):
    print("Interrupted.Saving...")
    result.to_csv("./结果.csv")
    print("Done.")
    sys.exit(1)


signal.signal(signal.SIGINT, caught_signal)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(build_random(2, 10))
    total2()
    # total()
