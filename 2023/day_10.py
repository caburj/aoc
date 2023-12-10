from utils import get_test_input, get_input
from itertools import product

# Pipe coordinates are (row_index, column_index).


N = "|F7"
E = "-7J"
W = "-LF"
S = "|LJ"

NS = set(product(N, S))
WE = set(product(W, E))
NE = set(product(N, E))
NW = set(product(N, W))
SE = set(product(S, E))
SW = set(product(S, W))


connections = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


def identify_start(neighbors):
    n, e, w, s = neighbors
    if (n, s) in NS:
        return "|"
    elif (w, e) in WE:
        return "-"
    elif (n, e) in NE:
        return "L"
    elif (n, w) in NW:
        return "J"
    elif (s, e) in SE:
        return "F"
    elif (s, w) in SW:
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

    topleft = (1, 1)
    bottomright = (height, width)

    sr, sc = find_start(grid, topleft, bottomright)
    neighbors = (grid[sr + r][sc + c] for r, c in [(-1, 0), (0, 1), (0, -1), (1, 0)])
    start_id = identify_start(neighbors)

    grid[sr] = grid[sr].replace("S", start_id)

    return grid, (sr, sc), topleft, bottomright


def find_start(grid, topleft, bottomright):
    start_r, start_c = topleft
    end_r, end_c = bottomright
    for row in range(start_r, end_r + 1):
        for col in range(start_c, end_c + 1):
            if grid[row][col] == "S":
                return row, col


def get_linked_parts(g, r, c):
    return [(r + i, c + j) for i, j in connections.get(g[r][c], [])]


def get_next(links, prev):
    return next(link for link in links if link != prev)


def find_loop(g, s):
    loop = [s]
    prev = s
    current = get_linked_parts(g, *s)[1]
    while current != s:
        temp = current
        loop.append(current)
        current = get_next(get_linked_parts(g, *current), prev)
        prev = temp
    return loop


def num_enclosed(g, s, tl, br):
    loop = find_loop(g, s)
    loop_set = set(loop)
    count = 0
    for i in range(tl[0], br[0] + 1):
        for j in range(tl[1], br[1] + 1):
            if (i, j) in loop_set:
                continue

            horizontal = sorted([(r, c) for r, c in loop if r == i], key=lambda x: x[1])
            vertical = sorted([(r, c) for r, c in loop if c == j], key=lambda x: x[0])

            r_pipes = [(r, c) for r, c in horizontal if c > j]
            l_pipes = [(r, c) for r, c in horizontal if c < j]
            t_pipes = [(r, c) for r, c in vertical if r < i]
            b_pipes = [(r, c) for r, c in vertical if r > i]

            n_intersections = [
                count_intersections(g, r_pipes, "-", "|"),
                count_intersections(g, l_pipes, "-", "|"),
                count_intersections(g, t_pipes, "|", "-"),
                count_intersections(g, b_pipes, "|", "-"),
            ]

            if not all(n_intersections):
                continue

            if any(x % 2 == 1 for x in n_intersections):
                count += 1

    return count


def count_intersections(g, items, to_ignore, to_count):
    n = 0
    ignore = False
    prev_ignored = None
    for r, c in items:
        p = g[r][c]
        if p == to_count:
            n += 1
            continue

        if ignore and p == to_ignore:
            continue

        match p, ignore, prev_ignored:
            case ("F", True, "J") | ("J", True, "F") | ("L", True, "7") | (
                "7",
                True,
                "L",
            ):
                n += 1
                prev_ignored = None
            case p, False, _:
                prev_ignored = p

        ignore = not ignore

    return n


if __name__ == "__main__":
    test_input = get_test_input(__file__)
    test_input_2 = get_test_input(__file__, "2")
    input = get_input(__file__)

    g1, s1, *_ = parse_input(test_input)
    g2, s2, *_ = parse_input(test_input_2)
    g, s, tl, br = parse_input(input)
    assert len(find_loop(g1, s1)) // 2 == 4
    assert len(find_loop(g2, s2)) // 2 == 8
    print("Part 1:", len(find_loop(g, s)) // 2)

    test_input_3 = get_test_input(__file__, "3")
    test_input_4 = get_test_input(__file__, "4")
    test_input_5 = get_test_input(__file__, "5")
    test_input_6 = get_test_input(__file__, "6")

    assert num_enclosed(*parse_input(test_input_3)) == 4
    assert num_enclosed(*parse_input(test_input_4)) == 4
    assert num_enclosed(*parse_input(test_input_5)) == 8
    assert num_enclosed(*parse_input(test_input_6)) == 10
    print("Part 2:", num_enclosed(g, s, tl, br))
