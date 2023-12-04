import os


def get_input_str(filename):
    input_file_name = filename.replace("day_", "input_").replace(".py", ".txt")
    full_file_name = os.path.join(os.path.dirname(filename), input_file_name)
    with open(full_file_name) as f:
        return f.read()


def get_input_test_str(filename):
    input_file_name = filename.replace("day_", "input_").replace(".py", "_test.txt")
    full_file_name = os.path.join(os.path.dirname(filename), input_file_name)
    with open(full_file_name) as f:
        return f.read()
