import networkx as nx
from utils import get_input, get_test_input, run


def parse_input(input):
    lines = input.splitlines()
    g = nx.Graph()
    for line in lines:
        source, target_str = line.split(":")
        for target in target_str.strip().split():
            g.add_edge(source, target)
    return g


def part_1(g):
    # By visual inspection, the graph is split into two components.
    # Use Girvan-Newman to find the clusters.
    x, y = next(nx.algorithms.community.girvan_newman(g))
    return len(x) * len(y)


def test():
    input = get_test_input(__file__)
    g = parse_input(input)
    assert part_1(g) == 54


def main():
    input = get_input(__file__)
    g = parse_input(input)
    print("Part 1:", part_1(g))


run(main, test, ignore_other_exceptions=False)
