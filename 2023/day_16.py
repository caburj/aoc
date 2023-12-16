import sys
from utils import get_test_input, get_input, run

sys.setrecursionlimit(999999)

NEXTS = {
    "|": {
        "left": ["up", "down"],
        "right": ["up", "down"],
    },
    "-": {
        "up": ["left", "right"],
        "down": ["left", "right"],
    },
    "/": {
        "up": ["right"],
        "down": ["left"],
        "left": ["down"],
        "right": ["up"],
    },
    "\\": {
        "up": ["left"],
        "down": ["right"],
        "left": ["up"],
        "right": ["down"],
    },
}

DELTAS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


def get_next(val, dir):
    return [dir] if val == "." else NEXTS[val].get(dir, [dir])


def parse_input(input):
    return [[[c, set()] for c in l] for l in input.strip().splitlines()]


def duplicate(contraption):
    return [[[c, set()] for c, _ in l] for l in contraption]


def count_illuminated(contraption):
    total = 0
    for l in contraption:
        for _, dirs in l:
            if len(dirs) > 0:
                total += 1
    return total


def _illuminate(contraption, start_row, start_col, direction):
    # TODO: REFACTOR: Don't use recursion.

    val, dirs = contraption[start_row][start_col]
    if direction in dirs:
        return

    dirs.add(direction)

    m = len(contraption)
    n = len(contraption[0])
    for next_dir in get_next(val, direction):
        dr, dc = DELTAS[next_dir]
        next_row = start_row + dr
        next_col = start_col + dc
        if 0 <= next_row < m and 0 <= next_col < n:
            _illuminate(contraption, next_row, next_col, next_dir)


def illuminate(contraption, start_row, start_col, direction):
    _illuminate(contraption, start_row, start_col, direction)
    return count_illuminated(contraption)


def get_optimized_illumination(contraption):
    m = len(contraption)
    n = len(contraption[0])
    starts = []
    for col in range(n):
        starts.append((0, col, "down"))
        starts.append((m - 1, col, "up"))

    for row in range(m):
        starts.append((row, 0, "right"))
        starts.append((row, n - 1, "left"))

    return max(illuminate(duplicate(contraption), *start) for start in starts)


def test():
    input = get_test_input(__file__)
    contraption = parse_input(input)
    assert illuminate(duplicate(contraption), 0, 0, "right") == 46
    assert get_optimized_illumination(duplicate(contraption)) == 51


def main():
    input = get_input(__file__)
    contraption = parse_input(input)
    print("Part 1:", illuminate(duplicate(contraption), 0, 0, "right"))
    print("Part 2:", get_optimized_illumination(duplicate(contraption)))


run(main, test)
