from utils import get_test_input, get_input, run

# All number of rows and columns are odd.


def find_vertical_mirror(rows, exclude=None):
    bounds = get_bounds(len(rows[0]))
    for loc, left, right in bounds:
        if exclude == loc:
            continue
        if all(is_mirrored(row, left, right) for row in rows):
            return loc
    return 0


def find_mirror_horizontal(rows, exclude=None):
    cols = [*zip(*rows)]
    return find_vertical_mirror(cols, exclude)


def get_bounds(n):
    middle = n // 2
    bounds = [(middle, (0, middle - 1), (middle, 2 * middle - 1))]
    for offset in range(1, middle):
        left = middle - offset
        bounds.append((left, (0, left - 1), (left, 2 * left - 1)))

    for offset in range(1, middle + 1):
        right = middle + offset
        x = n - right
        bounds.append((right, (right - x, right - 1), (right, n - 1)))

    return bounds


def is_mirrored(row, left, right):
    (a, b), (c, d) = left, right
    return row[a : b + 1] == row[c : d + 1][::-1]


def total_mirrors(patterns):
    result = 0
    for pattern in patterns:
        rows = pattern.strip().split("\n")
        result += find_vertical_mirror(rows)
        result += find_mirror_horizontal(rows) * 100
    return result


def flip(rows, i, j):
    if rows[i][j] == "#":
        rows[i][j] = "."
    else:
        rows[i][j] = "#"


def mirror_score_after_correction(record):
    rows = [list(x) for x in record.strip().split("\n")]
    original_v = find_vertical_mirror(rows)
    original_h = find_mirror_horizontal(rows)
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            flip(rows, i, j)

            new_v = find_vertical_mirror(rows, original_v)
            new_h = find_mirror_horizontal(rows, original_h)
            if new_v and original_h:
                return new_v
            if new_v and new_v != original_v:
                return new_v
            if new_h and original_v:
                return new_h * 100
            if new_h and new_h != original_h:
                return new_h * 100

            flip(rows, i, j)

    raise Exception("No correction found")


def total_corrected_mirrors(patterns):
    return sum(mirror_score_after_correction(pattern) for pattern in patterns)


def test():
    input = get_test_input(__file__)
    records = input.split("\n\n")
    assert total_mirrors(records) == 405
    assert total_corrected_mirrors(records) == 400


def main():
    input = get_input(__file__)
    records = input.split("\n\n")
    print("Part 1:", total_mirrors(records))
    print("Part 2:", total_corrected_mirrors(records))


run(main, test, ignore_other_exceptions=False)
