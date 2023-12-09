from utils import get_test_input, get_input


def parse_input(input):
    return [[int(x) for x in line.split(" ")] for line in input.splitlines()]


def get_deltas(start):
    yield start
    while any(start):
        yield (start := [b - a for a, b in zip(start, start[1:])])


def extrapolate(history, inverted):
    return sum(l[-1] for l in get_deltas(history[::-1] if inverted else history))


if __name__ == "__main__":
    test_histories = parse_input(get_test_input(__file__))
    histories = parse_input(get_input(__file__))

    part1_extrapolate = lambda h: extrapolate(h, False)
    assert sum(map(part1_extrapolate, test_histories)) == 114
    print("Part 1:", sum(map(part1_extrapolate, histories)))

    part2_extrapolate = lambda h: extrapolate(h, True)
    assert sum(map(part2_extrapolate, test_histories)) == 2
    print("Part 2:", sum(map(part2_extrapolate, histories)))
