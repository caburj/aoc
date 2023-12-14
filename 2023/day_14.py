from utils import get_test_input, get_input, run


def tilt_horizontal(lines, west=True):
    for i in range(len(lines)):
        line = lines[i]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            range_ = range(s + 1, e) if west else range(e - 1, s, -1)
            for j in range_:
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."


def tilt_vertical(lines, north=True):
    for j in range(len(lines[0])):
        line = [l[j] for l in lines]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            range_ = range(s + 1, e) if north else range(e - 1, s, -1)
            for i in range_:
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."


def cycle(lines):
    tilt_vertical(lines, north=True)
    tilt_horizontal(lines, west=True)
    tilt_vertical(lines, north=False)
    tilt_horizontal(lines, west=False)


def get_north_load(lines):
    result = 0
    n = len(lines[0]) - 2
    for i, line in enumerate(lines[1:-1]):
        n_O = len(list(filter(lambda x: x == "O", line)))
        factor = n - i
        result += n_O * factor
    return result


def parse_input(input):
    lines = [["#"] + list(line) + ["#"] for line in input.splitlines()]
    n = len(lines[0])
    lines.insert(0, ["#"] * n)
    lines.append(["#"] * n)
    return lines


def declare_incompetence():
    # I'm too lazy to find a way to do this programmatically.
    print(
        """
    Manually find the repeating pattern above.
        1. Find the start of the repeating pattern, call it S.
        2. Find the end of the repeating pattern, call it E.
        3. Frequency of the pattern is E - S + 1, as F.
        4. To get the value at 1_000_000_000, calculate (1_000_000_000 - S) % F as I.
        5. The value at 1_000_000_000 is the same as the value at S + I.
    """
    )


def test():
    lines = parse_input(get_test_input(__file__).strip())
    tilt_vertical(lines, north=True)
    assert get_north_load(lines) == 136

    lines = parse_input(get_test_input(__file__).strip())
    for i in range(0, 25):
        cycle(lines)
        print(f"{i + 1}:", get_north_load(lines))

    declare_incompetence()


def main():
    lines = parse_input(get_input(__file__).strip())
    tilt_vertical(lines, north=True)
    print("Part 1:", get_north_load(lines))

    lines = parse_input(get_input(__file__).strip())
    for i in range(1, 300):
        cycle(lines)
        print(f"{i}:", get_north_load(lines))

    declare_incompetence()


run(main, test)
