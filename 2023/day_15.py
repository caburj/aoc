import re
from functools import reduce
from utils import get_test_input, get_input, run


def hash(s):
    return reduce(lambda h, c: (h + ord(c)) * 17 % 256, s, 0)


def parse_commands(ss):
    return [re.compile(r"[-=]").split(s) for s in ss]


def run_commands(commands):
    boxes = [dict() for _ in range(256)]
    for command in commands:
        box, payload = command
        lenses = boxes[hash(box)]
        if payload == "":
            if box in lenses:
                del lenses[box]
        else:
            lenses[box] = int(payload)
    return boxes


def get_focusing_power(boxes):
    result = 0
    for box_id, lenses in enumerate(boxes):
        for slot_id, power in enumerate(lenses.values()):
            result += (box_id + 1) * (slot_id + 1) * power
    return result


def test():
    input = get_test_input(__file__).strip()
    ss = input.split(",")
    total_hash = sum(hash(s) for s in ss)
    assert total_hash == 1320
    assert get_focusing_power(run_commands(parse_commands(ss))) == 145


def main():
    input = get_input(__file__).strip()
    ss = input.split(",")
    total_hash = sum(hash(s) for s in ss)
    print("Part 1:", total_hash)
    print("Part 2:", get_focusing_power(run_commands(parse_commands(ss))))


run(main, test)
