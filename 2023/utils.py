import os


def read_file(filename, input_filename):
    full_file_name = os.path.join(os.path.dirname(filename), input_filename)
    with open(full_file_name) as f:
        return f.read()


def get_input(filename):
    input_name = filename.replace("day_", "input_").replace(".py", ".txt")
    return read_file(filename, input_name)


def get_test_input(filename, suffix=""):
    input_name = filename.replace("day_", "input_").replace(
        ".py", f"_test{suffix and f'_{suffix}'}.txt"
    )
    return read_file(filename, input_name)


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)
