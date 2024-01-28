from fractions import Fraction
from itertools import combinations
from utils import get_input, get_test_input, run

import z3


def parse_line(line):
    return tuple(map(parse_coords, line.strip().split("@")))


def parse_coords(string):
    return tuple(map(lambda x: int(x.strip()), string.strip().split(",")))


def line_eq(point, slope):
    x, y = point
    dx, dy = slope
    m = Fraction(dy, dx)
    b = y - m * x
    return m, b


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def future_intersect(line1, line2):
    p1, s1, (m1, b1) = line1
    p2, s2, (m2, b2) = line2
    if m1 == m2:
        return None
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    x1, y1 = p1
    dx1, dy1 = s1
    x2, y2 = p2
    dx2, dy2 = s2

    if (
        sign(x - x1) == sign(dx1)
        and sign(y - y1) == sign(dy1)
        and sign(x - x2) == sign(dx2)
        and sign(y - y2) == sign(dy2)
    ):
        return x, y


def get_2d_line(p3d, v3d):
    x, y, z = p3d
    dx, dy, dz = v3d
    p, s = (x, y), (dx, dy)
    return p, s, line_eq(p, s)


def parse_input(input):
    lines = input.splitlines()
    return list(map(parse_line, lines))


def count_intersections(lines, is_included):
    future_intersections = 0
    for line1, line2 in combinations(lines, 2):
        if line1 == line2:
            continue
        intersection = future_intersect(line1, line2)
        if intersection is None:
            continue

        x, y = intersection
        if is_included(x, y):
            future_intersections += 1
    return future_intersections


def find_magical_stone(hailstones):
    x, y, z, dx, dy, dz = z3.Ints("x y z dx dy dz")
    s = z3.Solver()
    for i, ((hx, hy, hz), (hdx, hdy, hdz)) in enumerate(hailstones):
        # need each hailstone to be hit by the "lazer" (magical stone)
        ti = z3.Int(f"t_{i}")
        s.add(ti > 0)
        s.add(x + dx * ti == hx + hdx * ti)
        s.add(y + dy * ti == hy + hdy * ti)
        s.add(z + dz * ti == hz + hdz * ti)

    if s.check() == z3.sat:
        m = s.model()
        x_val = m[x].as_long()
        y_val = m[y].as_long()
        z_val = m[z].as_long()
        return x_val + y_val + z_val


def test():
    input = get_test_input(__file__)
    lines = list(map(get_2d_line, *zip(*parse_input(input))))
    assert count_intersections(lines, lambda x, y: 7 <= x <= 27 and 7 <= y <= 27) == 2
    assert find_magical_stone(parse_input(input)) == 47


def main():
    input = get_input(__file__)
    lines = list(map(get_2d_line, *zip(*parse_input(input))))
    print(
        "Part 1:",
        count_intersections(
            lines,
            lambda x, y: 200000000000000 <= x <= 400000000000000
            and 200000000000000 <= y <= 400000000000000,
        ),
    )
    print("Part 2:", find_magical_stone(parse_input(input)))


run(main, test, ignore_other_exceptions=False)
