import re
from utils import get_input, get_test_input, run

# Directions:
#
#   0
# 3 + 1
#   2
DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
COMMAND_RE = re.compile(r"^([URDL])\s+(\d+)\s+\(#([0-9a-f]{6})\)$")
DIR_MAP = {"U": 0, "R": 1, "D": 2, "L": 3}

# Each corner needs to be adjusted by a certain amount to get the correct
# area. This table maps from the direction of the previous line to the
# direction of the next line to the adjustment needed.
#
# (from_dir, to_dir) -> (adjustment x, adjustment y)
ADJUSTMENTS = {
    (3, 2): (1, 1),
    (0, 1): (0, 0),
    (2, 1): (1, 0),
    (3, 0): (0, 1),
    (0, 3): (0, 1),
    (1, 2): (1, 0),
    (1, 0): (0, 0),
    (2, 3): (1, 1),
}


def parse_command(command_str):
    dir, dist, _ = COMMAND_RE.match(command_str).groups()
    return DIR_MAP[dir], int(dist)


def fixed_parse_command(command_str):
    *_, color = COMMAND_RE.match(command_str).groups()
    return (int(color[5]) + 1) % 4, int(color[:5], 16)


def get_corners(commands):
    n = len(commands)
    result = []
    current_x, current_y = 0, 0
    for i in range(len(commands)):
        from_i = i % n
        to_i = (i + 1) % n
        fdir, fdist = commands[from_i]
        tdir, _ = commands[to_i]
        (adj_x, adj_y) = ADJUSTMENTS[(fdir, tdir)]
        match fdir:
            case 0:
                current_y -= fdist
            case 1:
                current_x += fdist
            case 2:
                current_y += fdist
            case 3:
                current_x -= fdist
            case _:
                raise ValueError(f"Invalid direction: {fdir}")

        result.append((current_x + adj_x, current_y + adj_y))
    return result


def parse_input(input, fixed=False):
    lines = input.splitlines()
    commands = (
        [parse_command(x) for x in lines]
        if not fixed
        else [fixed_parse_command(x) for x in lines]
    )
    return list(get_corners(commands))


def shoe_lace(polygon):
    n = len(polygon)
    twice_area = 0
    for i in range(n - 1):
        j = (i + 1) % n
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        twice_area += xi * yj
        twice_area -= xj * yi
    return abs(twice_area) // 2


def test():
    input = get_test_input(__file__)

    lake = parse_input(input)
    print(lake)
    assert shoe_lace(lake) == 62

    fixed_lake = parse_input(input, fixed=True)
    assert shoe_lace(fixed_lake) == 952408144115


def main():
    input = get_input(__file__)

    lake = parse_input(input)
    print("Part 1:", shoe_lace(lake))

    fixed_lake = parse_input(input, fixed=True)
    print("Part 2:", shoe_lace(fixed_lake))


run(main, test, ignore_other_exceptions=False)
