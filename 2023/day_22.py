from utils import get_test_input, get_input, run


def parse_coord(str):
    return tuple(map(int, str.split(",")))


def parse_input(input):
    lines = input.splitlines()
    bricks = []
    for i, line in enumerate(lines):
        bricks.append((i + 1, tuple(map(parse_coord, line.split("~")))))

    def sort_key(brick):
        _, (start, end) = brick
        *_, sz = start
        *_, ez = end
        return (sz, ez)

    return sorted(bricks, key=sort_key)


def lay_bricks(bricks, m, n):
    # grid represents the relief of the floor
    grid = [list(0 for _ in range(n)) for _ in range(m)]
    cell_owner = [list(None for _ in range(n)) for _ in range(m)]
    # brick -> supports
    supports = {i: set() for i, brick in bricks}
    for i, ((sx, sy, sz), (ex, ey, ez)) in bricks:
        assert 0 <= sx < m and 0 <= sy < n and 0 <= ex < m and 0 <= ey < n

        if sx != ex:
            # laid along x axis
            # find max height of the grid along x axis where the brick will be laid
            max_height = max((row[sy] for row in grid[sx : ex + 1]))

            # max_height can't be equal or greater than sz
            assert max_height < sz

            # lay brick, put it on top of the grid
            for x in range(sx, ex + 1):
                if grid[x][sy] == max_height:  # it's a support
                    current_owner = cell_owner[x][sy]
                    if current_owner is not None:
                        supports[i].add(current_owner)

                grid[x][sy] = max_height + 1
                cell_owner[x][sy] = i

        elif sy != ey:
            # laid along y axis
            max_height = max(grid[sx][sy : ey + 1])

            assert max_height < sz

            for y in range(sy, ey + 1):
                if grid[sx][y] == max_height:
                    current_owner = cell_owner[sx][y]
                    if current_owner is not None:
                        supports[i].add(current_owner)

                grid[sx][y] = max_height + 1
                cell_owner[sx][y] = i
        else:
            # laid vertically
            # increase the height of the grid at sx, sy by the height of the brick
            brick_height = ez - sz + 1

            assert brick_height > 0

            current_owner = cell_owner[sx][sy]
            if current_owner is not None:
                supports[i].add(current_owner)

            grid[sx][sy] += brick_height
            cell_owner[sx][sy] = i

    supporting = {i: set() for i, _ in bricks}
    for i, _ in bricks:
        for j in supports[i]:
            supporting[j].add(i)

    return supports, supporting, bricks


def count_useless_bricks(supports, supporting, bricks):
    redundant_supports = set()
    not_supporting = set()
    for i, _ in bricks:
        _supporting = supporting[i]
        if not _supporting:
            not_supporting.add(i)
        else:
            if all(len(supports[j]) > 1 for j in _supporting):
                redundant_supports.add(i)

    return len(redundant_supports | not_supporting)


def find_affected_bricks(i, supports, supporting, destroyed):
    affected = set()
    for j in supporting[i]:
        j_supports = supports[j]
        remaining_supports = j_supports - destroyed
        if not remaining_supports:
            affected.add(j)
            destroyed.add(j)

    for j in supporting[i]:
        if j in affected:
            affected |= find_affected_bricks(j, supports, supporting, destroyed)

    return affected


def disintegrate(supports, supporting, bricks):
    return sum(
        len(find_affected_bricks(i, supports, supporting, {i})) for i, _ in bricks
    )


def test():
    input = get_test_input(__file__)
    floating_bricks = lay_bricks(parse_input(input), 10, 10)
    assert count_useless_bricks(*floating_bricks) == 5
    assert disintegrate(*floating_bricks) == 7


def main():
    input = get_input(__file__)
    floating_bricks = lay_bricks(parse_input(input), 10, 10)
    print("Part 1:", count_useless_bricks(*floating_bricks))
    print("Part 2:", disintegrate(*floating_bricks))


run(main, test, ignore_other_exceptions=False)
