import re
from utils import get_input, get_test_input

# Part 1:
# collect numbers
# each number will have a list of coordinates
# for each number, for each coordinate in that number
#   check adjacent coordinates if there is a symbol

is_symbol = lambda c: c != "."


def get_adjacent_coordinates(x_start, x_end, y, n_rows, n_cols):
    corners = [
        (x_start - 1, y - 1),
        (x_start - 1, y + 1),
        (x_end + 1, y - 1),
        (x_end + 1, y + 1),
    ]
    left = [(x_start - 1, y)]
    right = [(x_end + 1, y)]
    top = [(x, y - 1) for x in range(x_start, x_end + 1)]
    bottom = [(x, y + 1) for x in range(x_start, x_end + 1)]
    adjacent_cells = corners + left + right + top + bottom
    return [
        (x, y)
        for x, y in adjacent_cells
        if x >= 0 and y >= 0 and x < n_cols and y < n_rows
    ]


def find_row_numbers(row):
    for m in re.compile(r"\d+").finditer(row):
        yield (int(m.group()), (m.start(), m.end() - 1))


def find_numbers(grid):
    for y, row in enumerate(grid):
        for number, (x_start, x_end) in find_row_numbers(row):
            yield (number, y, (x_start, x_end))


def find_valid_numbers(grid):
    for number, y, (x_start, x_end) in find_numbers(grid):
        adjacent_coordinates = get_adjacent_coordinates(
            x_start, x_end, y, len(grid), len(grid[0])
        )
        if any(is_symbol(grid[y][x]) for x, y in adjacent_coordinates):
            yield number


def get_asterisk_coordinates(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "*":
                yield (x, y)


def get_gears(grid):
    asterisk_coords = get_asterisk_coordinates(grid)
    for asterisk_coord in asterisk_coords:
        group = []
        for number, y, (x_start, x_end) in find_numbers(grid):
            adjacent_coordinates = get_adjacent_coordinates(
                x_start, x_end, y, len(grid), len(grid[0])
            )
            if asterisk_coord in adjacent_coordinates:
                group.append(number)
        if len(group) == 2:
            yield tuple(group)


input_test_str = get_test_input(__file__).strip()
test_grid = input_test_str.splitlines()
assert sum(find_valid_numbers(test_grid)) == 4361
assert sum((g1 * g2 for g1, g2 in get_gears(test_grid))) == 467835

input_str = get_input(__file__).strip()
grid = input_str.splitlines()
print("Part 1:", sum(find_valid_numbers(grid)))
print("Part 2:", sum((g1 * g2 for g1, g2 in get_gears(grid))))
