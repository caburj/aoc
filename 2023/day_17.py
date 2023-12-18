import sys
import math
from utils import get_test_input, get_input, run

# Directions:
#
#   0
# 3 + 1
#   2
DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
SYMBOLS = ["^", ">", "v", "<"]


def turn_left(dir):
    return (dir - 1) % 4


def turn_right(dir):
    return (dir + 1) % 4


class Graph:
    def __init__(self, input):
        self.map = [[int(x) for x in line] for line in input.splitlines()]
        self.n_rows = len(self.map)
        self.n_cols = len(self.map[0])

    def get_turns(self, u):
        i, j, d, _ = u

        for new_dir in [turn_left(d), turn_right(d)]:
            di, dj = DELTAS[new_dir]
            vi = i + di
            vj = j + dj
            if 0 <= vi < self.n_rows and 0 <= vj < self.n_cols:
                yield (vi, vj, new_dir, 1)

    def get_forward(self, u):
        i, j, d, f = u

        di, dj = DELTAS[d]
        vi = i + di
        vj = j + dj
        if 0 <= vi < self.n_rows and 0 <= vj < self.n_cols:
            yield (vi, vj, d, f + 1)

    def get_neighbors_1(self, u):
        *_, uf = u

        yield from self.get_turns(u)

        if uf != 3:
            yield from self.get_forward(u)

    def get_neighbors_2(self, u):
        *_, uf = u

        # can only move forward if uf < 4
        # can only turn left or right if uf == 10

        if uf < 10:
            yield from self.get_forward(u)

        if uf >= 4:
            yield from self.get_turns(u)

    def get_neighbors(self, u, strategy):
        if strategy == 1:
            return self.get_neighbors_1(u)
        elif strategy == 2:
            return self.get_neighbors_2(u)
        else:
            raise ValueError("Unknown strategy")

    def find_optimum_path(self, strategy):
        starts = [(0, 0, 1, 1), (0, 0, 2, 1)]

        dist = dict((s, 0) for s in starts)
        prev = dict((s, None) for s in starts)

        # TODO: use a priority queue
        Q = set(starts)

        while Q:
            u = min(Q, key=lambda x: dist.get(x, math.inf))
            Q.remove(u)

            for v in self.get_neighbors(u, strategy):
                vi, vj, *_ = v

                alt = dist[u] + self.map[vi][vj]
                if alt < dist.get(v, math.inf):
                    dist[v] = alt
                    prev[v] = u
                    Q.add(v)

        ei = len(self.map) - 1
        ej = len(self.map[0]) - 1
        end = min([x for x in dist if x[0] == ei and x[1] == ej], key=lambda x: dist[x])

        path = []
        u = end
        while prev[u]:
            path.append(u)
            u = prev[u]
        path.append(u)
        path.reverse()

        return path, dist[end]

    def draw_path(self, path):
        map = [["."] * self.n_cols for _ in range(self.n_rows)]
        for i, j, d, _ in path:
            map[i][j] = SYMBOLS[d]
        print("\n".join(["".join(row) for row in map]))


def test():
    input = get_test_input(__file__)
    city_map = Graph(input)
    path, dist = city_map.find_optimum_path(strategy=1)
    city_map.draw_path(path)
    assert dist == 102
    path2, dist2 = city_map.find_optimum_path(strategy=2)
    city_map.draw_path(path2)
    assert dist2 == 94


def main():
    input = get_input(__file__)
    city_map = Graph(input)
    path, dist = city_map.find_optimum_path(strategy=1)
    city_map.draw_path(path)
    print("Part 1:", dist)
    path2, dist2 = city_map.find_optimum_path(strategy=2)
    city_map.draw_path(path2)
    print("Part 2:", dist2)


run(main, test, ignore_other_exceptions=False)
