from itertools import combinations
from utils import get_test_input, get_input, run


def find_galaxies(grid, m):
    # m = expansion factor
    row_gaps = [i for i, row in enumerate(grid) if row.count("#") == 0]
    col_gaps = [j for j, col in enumerate(zip(*grid)) if col.count("#") == 0]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                n_row_gaps = len([g for g in row_gaps if g < i])
                n_col_gaps = len([g for g in col_gaps if g < j])
                expanded_i = n_row_gaps * m + (i - n_row_gaps)
                expanded_j = n_col_gaps * m + (j - n_col_gaps)
                yield (expanded_i, expanded_j)


def total_distance(galaxies):
    pairs = combinations(galaxies, 2)
    return sum(abs(r1 - r2) + abs(c1 - c2) for (r1, c1), (r2, c2) in pairs)


def test():
    test_grid = get_test_input(__file__).splitlines()
    assert total_distance(find_galaxies(test_grid, 2)) == 374
    assert total_distance(find_galaxies(test_grid, 10)) == 1030
    assert total_distance(find_galaxies(test_grid, 100)) == 8410


def main():
    grid = get_input(__file__).splitlines()
    print("Part 1:", total_distance(find_galaxies(grid, 2)))
    print("Part 2:", total_distance(find_galaxies(grid, 1_000_000)))


run(main, test)
