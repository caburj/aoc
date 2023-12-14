from utils import get_test_input, get_input, run


def tilt_north(lines):
    for j in range(len(lines[0])):
        line = [l[j] for l in lines]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            for i in range(s + 1, e):
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."


def cycle(lines):
    n_cols = len(lines[0])
    n_rows = len(lines)

    tilt_north(lines)

    # tilt west
    for i in range(n_rows):
        line = lines[i]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            for j in range(s + 1, e):
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."

    # tilt south
    for j in range(n_cols):
        line = [l[j] for l in lines]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            for i in range(e - 1, s, -1):
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."

    # tilt east
    for i in range(n_rows):
        line = lines[i]
        box_ids = [i for i, x in enumerate(line) if x == "#"]
        for s, e in zip(box_ids, box_ids[1:]):
            n_O = len(list(filter(lambda x: x == "O", line[s + 1 : e])))
            n_placed_O = 0
            for j in range(e - 1, s, -1):
                if n_placed_O < n_O:
                    lines[i][j] = "O"
                    n_placed_O += 1
                else:
                    lines[i][j] = "."


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


def draw(lines):
    return "\n".join("".join(line) for line in lines)


def test():
    lines = parse_input(get_test_input(__file__).strip())
    tilt_north(lines)
    assert get_north_load(lines) == 136

    lines = parse_input(get_test_input(__file__).strip())
    for i in range(0, 25):
        cycle(lines)
        print(f"{i + 1}:", get_north_load(lines))

    print(
        """
        Manually check the repeating pattern above.
        1. Find the start of the repeating pattern, call it S.
        2. Find the end of the repeating pattern, call it E.
        3. Frequency of the pattern is E - S + 1.
        4. To get the value at 1_000_000_000, calculate (1_000_000_000 - S) % (E - S + 1) as I.
        5. The value at 1_000_000_000 is the same as the value at S + I.
    """
    )


def main():
    lines = parse_input(get_input(__file__).strip())
    print("Part 1:", get_north_load(lines))

    lines = parse_input(get_input(__file__).strip())
    for i in range(1, 1000):
        cycle(lines)
        print(f"{i}:", get_north_load(lines))

    print(
        """
        Manually check the repeating pattern above.
        1. Find the start of the repeating pattern, call it S.
        2. Find the end of the repeating pattern, call it E.
        3. Frequency of the pattern is E - S + 1.
        4. To get the value at 1_000_000_000, calculate (1_000_000_000 - S) % (E - S + 1) as I.
        5. The value at 1_000_000_000 is the same as the value at S + I.
    """
    )


run(main, test)
