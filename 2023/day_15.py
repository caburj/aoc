from utils import get_test_input, get_input, run


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def parse_commands(ss):
    commands = []
    for s in ss:
        if "=" in s:
            box_hash, payload = s.split("=")
            commands.append((box_hash, "=", int(payload)))
        else:
            box_hash, _ = s.split("-")
            commands.append((box_hash, "-", None))
    return commands


def run_commands(commands):
    boxes = [dict() for _ in range(256)]
    for command in commands:
        box_hash, op, payload = command
        box_id = hash(box_hash)
        lenses = boxes[box_id]
        if op == "-":
            if box_hash in lenses:
                del lenses[box_hash]
        else:
            lenses[box_hash] = payload
    return boxes


def get_focusing_power(boxes):
    result = 0
    for box_id, lenses in enumerate(boxes):
        for slot_id, (_box_hash, power) in enumerate(lenses.items()):
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
