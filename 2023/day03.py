import re

number_re = re.compile(r'\d+')

sample = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()

# Part 1:
# collect numbers
# each number will have a list of coordinates
# for each number, for each coordinate in that number
#   check adjacent coordinates if there is a symbol

def get_adjacent_coordinates(start_col, end_col, y, n_rows, n_cols):
    corners = [
        (start_col - 1, y - 1),
        (start_col - 1, y + 1),
        (end_col + 1, y - 1),
        (end_col + 1, y + 1)
    ]
    left = [(start_col - 1, y)]
    right = [(end_col + 1, y)]
    top = [(x, y - 1) for x in range(start_col, end_col + 1)]
    bottom = [(x, y + 1) for x in range(start_col, end_col + 1)]
    adjacent_cells = corners + left + right + top + bottom
    return [
        (x, y)
        for x, y in adjacent_cells
        if x >= 0 and y >= 0 and x < n_cols and y < n_rows
    ]

def is_symbol(c):
    return c != '.'

def find_row_numbers(row):
    # result := List<(number: int, (start_col: int, end_col: int))>
    result = []
    for m in number_re.finditer(row):
        start = m.start()
        end = m.end()
        number = int(row[start:end])
        result.append((number, (start, end - 1)))
    return result

def find_numbers(grid):
    # result := List<(number: int, (start_col: int, end_col: int), row: int)>
    result = []
    for y, row in enumerate(grid):
        for number, (start_col, end_col) in find_row_numbers(row):
            result.append((number, y, (start_col, end_col)))
    return result

def find_valid_numbers(grid):
    # result := List<number>
    n_rows = len(grid)
    n_cols = len(grid[0])
    result = []
    numbers = find_numbers(grid)
    for number, y, (start_col, end_col) in numbers:
        adjacent_coordinates = get_adjacent_coordinates(start_col, end_col, y, n_rows, n_cols)
        if any(is_symbol(grid[y][x]) for x, y in adjacent_coordinates):
            result.append(number)
    return result

def get_asterisk_coordinates(grid):
    # result := List<(x: int, y: int)>
    result = []
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '*':
                result.append((x, y))
    return result

def get_gears(grid):
    asterisk_coords = get_asterisk_coordinates(grid)
    numbers = find_numbers(grid)
    n_rows = len(grid)
    n_cols = len(grid[0])
    gears = [] # List<List<number>>
    for asterisk in asterisk_coords:
        group = []
        for number, y, (start_col, end_col) in numbers:
            adjacent_coordinates = get_adjacent_coordinates(start_col, end_col, y, n_rows, n_cols)
            if asterisk in adjacent_coordinates:
                group.append(number)
        if (len(group) == 2):
            gears.append(group)
    return gears

def sum_numbers(grid):
    return sum(find_valid_numbers(grid))

def test_sum_numbers():
    grid = sample.split('\n')
    assert sum_numbers(grid) == 4361

def test_gears():
    grid = sample.split('\n')
    gears = get_gears(grid)
    total_gear_ratio = sum((g1 * g2 for g1, g2 in gears))
    assert total_gear_ratio == 467835

test_sum_numbers()
test_gears()

with open('2023/day03.txt') as f:
    grid = f.read().strip().split('\n')
    print('Part 1:', sum_numbers(grid))
    print('Part 2:', sum((g1 * g2 for g1, g2 in get_gears(grid))))
