import re


def is_valid_hexa_code(string):
    hexa_code = re.compile(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')
    return bool(re.match(hexa_code, string))

string = "#100"

print(is_valid_hexa_code(string))