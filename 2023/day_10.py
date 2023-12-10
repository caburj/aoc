from utils import get_test_input, get_input

# coordinates are (row, col)

connections = {
    ".": [],
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


def identify_start(neighbors):
    n, e, w, s = neighbors
    if n == "|" and s == "|":
        return "|"
    elif e == "-" and w == "-":
        return "-"
    elif n == "|" and e == "-":
        return "L"
    elif n == "|" and w == "-":
        return "J"
    elif s == "|" and e == "-":
        return "F"
    elif s == "|" and w == "-":
        return "7"
    elif e == "J" and s == "|":
        return "F"
    elif w == "L" and n == "F":
        return "J"
    elif e == "7" and s == "J":
        return "F"
    elif w == "F" and s == "|":
        return "7"
    else:
        raise ValueError("start is not connected")


def parse_input(input):
    # wrap . around the grid
    # return original grid's bounds
    grid = []
    lines = input.splitlines()
    width = len(lines[0])
    height = len(lines)
    grid.append("." * (width + 2))
    for line in lines:
        grid.append("." + line + ".")
    grid.append("." * (width + 2))
    return grid, (1, 1), (height, width)


def find_start(grid, topleft, bottomright, start_char):
    sr, sc = topleft
    er, ec = bottomright
    for row in range(sr, er + 1):
        for col in range(sc, ec + 1):
            if grid[row][col] == start_char:
                return row, col


def get_all_neighbors(grid, row, col):
    return (grid[row + r][col + c] for r, c in [(-1, 0), (0, 1), (0, -1), (1, 0)])


def get_linked_parts(g, r, c, part, start):
    sr, sc, sp = start
    return [
        (r + i, c + j, sp if r + i == sr and c + j == sc else g[r + i][c + j])
        for i, j in connections[part]
    ]


def get_next(links, prev):
    return next(link for link in links if link != prev)


def find_loop(g, tl, br):
    start = find_start(g, tl, br, "S")
    neighbors = get_all_neighbors(g, *start)
    start_part = identify_start(neighbors)
    _start = (*start, start_part)
    loop = [_start]
    prev = _start
    current = get_linked_parts(g, *_start, _start)[1]
    while current != _start:
        temp = current
        loop.append(current)
        current = get_next(get_linked_parts(g, *current, _start), prev)
        prev = temp

    return loop


def num_enclosed(g, tl, br):
    loop = find_loop(g, tl, br)
    set_loop = set(loop)
    count = 0
    for i in range(tl[0], br[0] + 1):
        for j in range(tl[1], br[1] + 1):
            if g[i][j] == "S" or (i, j, g[i][j]) in set_loop:
                continue

            rights = chi(sorted([(r, c, p) for r, c, p in loop if c > j and r == i], key=lambda x: x[1]), i, j)
            lefts = chi(sorted([(r, c, p) for r, c, p in loop if c < j and r == i], key=lambda x: -x[1]), i, j)
            ups = cvi(sorted([(r, c, p) for r, c, p in loop if r < i and c == j], key=lambda x: -x[0]), i, j)
            downs = cvi(sorted([(r, c, p) for r, c, p in loop if r > i and c == j], key=lambda x: x[0]), i, j)

            if any(x == 0 for x in [rights, lefts, ups, downs]):
                continue

            if any(x % 2 == 1 for x in [rights, lefts, ups, downs]):
                count += 1

    return count


def cvi(items, i, j):
    # Count Vertical Intersections
    n = 0
    ignore = False
    prev_ignored = None
    for r, c, p in items:
        if p == "-":
            n += 1
            continue

        if ignore and p == "|":
            continue

        if p == "F":
            if ignore:
                if prev_ignored == "J":
                    n += 1
                elif prev_ignored == "L":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "F"

        elif p == "L":
            if ignore:
                if prev_ignored == "7":
                    n += 1
                elif prev_ignored == "F":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "L"

        elif p == "7":
            if ignore:
                if prev_ignored == "L":
                    n += 1
                elif prev_ignored == "J":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "7"

        elif p == "J":
            if ignore:
                if prev_ignored == "F":
                    n += 1
                elif prev_ignored == "7":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "J"

    return n


def chi(items, i, j):
    # Count Horizontal Intersections
    n = 0
    ignore = False
    prev_ignored = None
    for r, c, p in items:
        if p == "|":
            n += 1
            continue

        if ignore and p == "-":
            continue

        if p == "F":
            if ignore:
                if prev_ignored == "J":
                    n += 1
                elif prev_ignored == "7":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "F"

        elif p == "L":
            if ignore:
                if prev_ignored == "7":
                    n += 1
                elif prev_ignored == "J":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "L"

        elif p == "7":
            if ignore:
                if prev_ignored == "L":
                    n += 1
                elif prev_ignored == "F":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "7"

        elif p == "J":
            if ignore:
                if prev_ignored == "F":
                    n += 1
                elif prev_ignored == "L":
                    n += 0
                else:
                    print(i, j, r, c, p, prev_ignored)

                ignore = False
                prev_ignored = None
            else:
                ignore = True
                prev_ignored = "J"

    return n


if __name__ == "__main__":
    test_input = get_test_input(__file__)
    test_input_2 = get_test_input(__file__, "2")

    input = get_input(__file__)
    assert len(find_loop(*parse_input(test_input))) // 2 == 4
    assert len(find_loop(*parse_input(test_input_2))) // 2 == 8
    print("Part 1:", len(find_loop(*parse_input(input))) // 2)

    test_input_3 = get_test_input(__file__, "3")
    test_input_4 = get_test_input(__file__, "4")
    test_input_5 = get_test_input(__file__, "5")
    test_input_6 = get_test_input(__file__, "6")

    assert num_enclosed(*parse_input(test_input_3)) == 4
    assert num_enclosed(*parse_input(test_input_4)) == 4
    assert num_enclosed(*parse_input(test_input_5)) == 8
    assert num_enclosed(*parse_input(test_input_6)) == 10
    print("Part 2:", num_enclosed(*parse_input(input)))
