from collections import deque
from utils import get_input, get_test_input, run


class Map:
    def __init__(self, input):
        lines = input.splitlines()
        self.map = lines
        self.r = len(lines)
        self.c = len(lines[0])
        self.s = self.find_start()

    def find_start(self):
        for i in range(self.r):
            for j in range(self.c):
                if self.map[i][j] == "S":
                    return i, j

    def check(self, i, j):
        if 0 <= i < self.r and 0 <= j < self.c and self.map[i][j] != "#":
            return (i, j)

    def up(self, i, j):
        return self.check(i - 1, j)

    def down(self, i, j):
        return self.check(i + 1, j)

    def left(self, i, j):
        return self.check(i, j - 1)

    def right(self, i, j):
        return self.check(i, j + 1)

    def get_neighbors(self, i, j):
        for f in [self.up, self.down, self.left, self.right]:
            d = f(i, j)
            if d:
                yield d

    def bfs(self, max_steps):
        step = 0
        q = deque([self.s])
        while True:
            step = step + 1
            next_q = deque()
            in_q = set()
            while q:
                (i, j) = q.popleft()
                for n in self.get_neighbors(i, j):
                    if not n in in_q:
                        in_q.add(n)
                        next_q.append(n)

            if step == max_steps:
                return self.count_possible_last_locations(next_q)
            else:
                q = next_q

    def count_possible_last_locations(self, q):
        return len(set(q))


def test():
    input = get_test_input(__file__)
    map = Map(input)
    assert map.bfs(6) == 16


def main():
    input = get_input(__file__)
    map = Map(input)
    print("Part 1:", map.bfs(64))


run(main, test, ignore_other_exceptions=False)
