import re
from itertools import cycle
from functools import reduce
from utils import get_test_input, get_input, lcm

node_re = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def parse_input(input):
    steps, nodes_str = input.split("\n\n")
    nodes = {name: (x, y) for name, x, y in node_re.findall(nodes_str)}
    return steps, nodes


def choose_next(node, step):
    return step == "L" and node[0] or node[1]


def trace(steps, nodes, start, is_end):
    current = start
    for i, step in enumerate(cycle(steps)):
        current = choose_next(nodes[current], step)
        if is_end(current):
            return i + 1


def parallel_trace(steps, nodes, start_suffix, end_suffix):
    starts = [key for key in nodes if key.endswith(start_suffix)]
    ends = {key for key in nodes if key.endswith(end_suffix)}
    is_end = lambda node: node in ends
    return reduce(lcm, map(lambda start: trace(steps, nodes, start, is_end), starts))


if __name__ == "__main__":
    test_steps, test_nodes = parse_input(get_test_input(__file__))
    basic_is_end = lambda node: node == "ZZZ"
    assert trace(test_steps, test_nodes, "AAA", basic_is_end) == 6
    steps, nodes = parse_input(get_input(__file__))
    print("Part 1:", trace(steps, nodes, "AAA", basic_is_end))
    test_steps2, test_nodes2 = parse_input(get_test_input(__file__, "2"))
    assert parallel_trace(test_steps2, test_nodes2, "A", "Z") == 6
    print("Part 2:", parallel_trace(steps, nodes, "A", "Z"))
