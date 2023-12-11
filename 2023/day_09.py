from utils import get_test_input, get_input, run


def parse_input(input):
    return [[int(x) for x in line.split(" ")] for line in input.splitlines()]


def get_deltas(start):
    yield start
    while any(start):
        yield (start := [b - a for a, b in zip(start, start[1:])])


def extrapolate(history, inverted):
    return sum(l[-1] for l in get_deltas(history[::-1] if inverted else history))


part1_extrapolate = lambda h: extrapolate(h, False)
part2_extrapolate = lambda h: extrapolate(h, True)


def test():
    test_histories = parse_input(get_test_input(__file__))
    assert sum(map(part1_extrapolate, test_histories)) == 114
    assert sum(map(part2_extrapolate, test_histories)) == 2


def main():
    histories = parse_input(get_input(__file__))
    print("Part 1:", sum(map(part1_extrapolate, histories)))
    print("Part 2:", sum(map(part2_extrapolate, histories)))


run(main, test)
