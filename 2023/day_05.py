import re
from functools import reduce
from utils import get_test_input, get_input

number_re = re.compile(r"\d+")


def find_ints(string):
    return [int(x) for x in re.findall(number_re, string)]


def make_mapper(block: str, invert=False):
    lines = block.splitlines()
    map_specs = [find_ints(line) for line in lines[1:]]

    def mapper(seed):
        for dest, source, range in map_specs:
            if invert:
                dest, source = source, dest
            if seed >= source and seed < source + range:
                return dest + (seed - source)
        return seed

    return mapper


def locate(mappers, seed):
    # mappers: Array<Array<[dest: int, source: int, range: int]>>
    return reduce(lambda seed, mapper: mapper(seed), mappers, seed)


def parse_input(input, invert_mappers=False):
    blocks = input.split("\n\n")
    seeds = find_ints(blocks[0])
    mappers = [make_mapper(block, invert_mappers) for block in blocks[1:]]
    return seeds, mappers


def part1(input):
    seeds, mappers = parse_input(input)
    return min(locate(mappers, seed) for seed in seeds)


def part2(input):
    """Invert the search.

    - Iterate over possible locations starting from 0.
        - For each location, check if its corresponding seed is in the seed ranges.
        - Return the first one to be found.

    This is still slow and uncertain, but it will give result within a few minutes.
    Contrast this with the original search (seed-to-location), which might not even finish.
    """

    seeds, mappers = parse_input(input, True)
    seed_ranges = [*zip(seeds[::2], seeds[1::2])]
    inv_mappers = mappers[::-1]
    i = 0
    while True:
        seed = locate(inv_mappers, i)
        if any(start <= seed < start + n for start, n in seed_ranges):
            return i
        if i > 0 and (i % 10000000) == 0:
            print("Searching", i, "...")
        i += 1

test_input = get_test_input(__file__)
if test_input:
    assert part1(test_input) == 35
    assert part2(test_input) == 46

input = get_input(__file__)
print("Part 1:", part1(input))
print("Part 2:", part2(input))
