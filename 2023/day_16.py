import sys
from itertools import chain
from utils import get_test_input, get_input, run

sys.setrecursionlimit(999999)

NEXTS = {
    "|": {
        "L": ["U", "D"],
        "R": ["U", "D"],
    },
    "-": {
        "U": ["L", "R"],
        "D": ["L", "R"],
    },
    "/": {
        "U": ["R"],
        "D": ["L"],
        "L": ["D"],
        "R": ["U"],
    },
    "\\": {
        "U": ["L"],
        "D": ["R"],
        "L": ["U"],
        "R": ["D"],
    },
}

DELTAS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def get_next(val, dir):
    return [dir] if val == "." else NEXTS[val].get(dir, [dir])


def parse_input(input):
    return [[[c, set()] for c in l] for l in input.strip().splitlines()]


def copy(contraption):
    return [[[c, set()] for c, _ in l] for l in contraption]


def count_illuminated(contraption):
    return len(list(filter(lambda x: len(x[1]) > 0, chain(*contraption))))


def _illuminate(contraption, row, col, direction):
    # TODO: REFACTOR: Don't use recursion. Convert to iterative solution.

    val, dirs = contraption[row][col]
    if direction in dirs:
        return

    dirs.add(direction)

    m = len(contraption)
    n = len(contraption[0])
    for next_dir in get_next(val, direction):
        dr, dc = DELTAS[next_dir]
        next_row = row + dr
        next_col = col + dc
        if 0 <= next_row < m and 0 <= next_col < n:
            _illuminate(contraption, next_row, next_col, next_dir)


def illuminate(contraption, start_row, start_col, direction):
    _illuminate(contraption, start_row, start_col, direction)
    return count_illuminated(contraption)


def find_max_illumination(contraption):
    m = len(contraption)
    n = len(contraption[0])
    starts = [
        *chain(*[[(0, j, "D"), (m - 1, j, "U")] for j in range(n)]),
        *chain(*[[(i, 0, "R"), (i, n - 1, "L")] for i in range(m)]),
    ]
    return max(illuminate(copy(contraption), *start) for start in starts)


def test():
    input = get_test_input(__file__)
    contraption = parse_input(input)
    assert illuminate(copy(contraption), 0, 0, "R") == 46
    assert find_max_illumination(copy(contraption)) == 51


def main():
    input = get_input(__file__)
    contraption = parse_input(input)
    print("Part 1:", illuminate(copy(contraption), 0, 0, "R"))
    print("Part 2:", find_max_illumination(copy(contraption)))


run(main, test)
