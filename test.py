import numpy as np

from common import *

# oh yeah lol I was looking into hex code validation
'''
import re


def is_valid_hexa_code(string):
    hexa_code = re.compile(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')
    return bool(re.match(hexa_code, string))

string = "#100"
print(is_valid_hexa_code(string))
'''


my_list = [1, 2, 3, 4, 5]

shuffled_list = sorted(my_list, key=lambda x: random.random())

print("Original list:", my_list)
print("Shuffled list:", shuffled_list)
