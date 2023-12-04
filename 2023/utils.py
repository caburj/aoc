import os


def read_file(filename, input_filename):
    full_file_name = os.path.join(os.path.dirname(filename), input_filename)
    with open(full_file_name) as f:
        return f.read()


def get_input(filename):
    input_name = filename.replace("day_", "input_").replace(".py", ".txt")
    return read_file(filename, input_name)


def get_test_input(filename):
    input_name = filename.replace("day_", "input_").replace(".py", "_test.txt")
    return read_file(filename, input_name)
