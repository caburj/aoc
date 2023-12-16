import sys
from utils import get_test_input, get_input, run

sys.setrecursionlimit(999999)


def get_deltas(current_position, direction):
    match current_position:
        case ".":
            match direction:
                case "up":
                    return [(-1, 0, "up")]
                case "down":
                    return [(1, 0, "down")]
                case "left":
                    return [(0, -1, "left")]
                case "right":
                    return [(0, 1, "right")]
        case "|":
            match direction:
                case "up":
                    return [(-1, 0, "up")]
                case "down":
                    return [(1, 0, "down")]
                case "left" | "right":
                    return [(1, 0, "down"), (-1, 0, "up")]
        case "-":
            match direction:
                case "left":
                    return [(0, -1, "left")]
                case "right":
                    return [(0, 1, "right")]
                case "up" | "down":
                    return [(0, 1, "right"), (0, -1, "left")]
        case "/":
            match direction:
                case "up":
                    return [(0, 1, "right")]
                case "down":
                    return [(0, -1, "left")]
                case "left":
                    return [(1, 0, "down")]
                case "right":
                    return [(-1, 0, "up")]
        case "\\":
            match direction:
                case "up":
                    return [(0, -1, "left")]
                case "down":
                    return [(0, 1, "right")]
                case "left":
                    return [(-1, 0, "up")]
                case "right":
                    return [(1, 0, "down")]

    raise Exception("Unknown direction: " + direction)


def get_contraption(input):
    return [[[c, set()] for c in l] for l in input.strip().splitlines()]


def duplicate(contraption):
    return [[[c, set()] for c, _ in l] for l in contraption]


def draw(contraption):
    print(
        "\n".join("".join(c if len(x) == 0 else "#" for c, x in l) for l in contraption)
    )
    print()


def count_illuminated(contraption):
    total = 0
    for l in contraption:
        for _, dirs in l:
            if len(dirs) > 0:
                total += 1
    return total


def illuminate(contraption, start_row, start_col, direction):
    val, dirs = contraption[start_row][start_col]
    if direction in dirs:
        return

    dirs.add(direction)

    deltas = get_deltas(val, direction)
    m = len(contraption)
    n = len(contraption[0])
    for dr, dc, dir in deltas:
        next_row = start_row + dr
        next_col = start_col + dc
        if 0 <= next_row < m and 0 <= next_col < n:
            illuminate(contraption, next_row, next_col, dir)


def get_optimized_illumination(contraption):
    optimum_illumination = 0
    m = len(contraption)
    n = len(contraption[0])
    for col in range(n):
        dcon = duplicate(contraption)
        illuminate(dcon, 0, col, "down")
        illumination = count_illuminated(dcon)
        if illumination > optimum_illumination:
            optimum_illumination = illumination

        dcon = duplicate(contraption)
        illuminate(dcon, m - 1, col, "up")
        illumination = count_illuminated(dcon)
        if illumination > optimum_illumination:
            optimum_illumination = illumination

    for row in range(m):
        dcon = duplicate(contraption)
        illuminate(dcon, row, 0, "right")
        illumination = count_illuminated(dcon)
        if illumination > optimum_illumination:
            optimum_illumination = illumination

        dcon = duplicate(contraption)
        illuminate(dcon, row, n - 1, "left")
        illumination = count_illuminated(dcon)
        if illumination > optimum_illumination:
            optimum_illumination = illumination

    return optimum_illumination


def test():
    input = get_test_input(__file__)
    contraption = get_contraption(input)
    illuminate(contraption, 0, 0, "right")
    assert count_illuminated(contraption) == 46
    assert get_optimized_illumination(get_contraption(input)) == 51


def main():
    input = get_input(__file__)
    contraption = get_contraption(input)
    illuminate(contraption, 0, 0, "right")
    print("Part 1:", count_illuminated(contraption))
    print("Part 2:", get_optimized_illumination(get_contraption(input)))


run(main, test, ignore_other_exceptions=False)
