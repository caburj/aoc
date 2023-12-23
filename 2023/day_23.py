from utils import get_input, get_test_input, run


class Graph:
    def __init__(self, input):
        self.grid = input.splitlines()
        self.m = len(self.grid)
        self.n = len(self.grid[0])

        self.start_node = (0, 1)
        self.end_node = len(self.grid) - 1, len(self.grid[0]) - 2

        self.construct_graph()

    def construct_graph(self):
        self.graph = {}

        # nodes include the start and end nodes, and coordinates where at least one of the neighbors is one of "<>^v"
        nodes = set([self.start_node, self.end_node])
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] != ".":
                    continue

                surrounding_slopes = 0
                for ni, nj in self.get_neighbors((i, j)):
                    if self.grid[ni][nj] in "<>^v":
                        surrounding_slopes += 1

                if surrounding_slopes == 4 or surrounding_slopes == 3:
                    nodes.add((i, j))

        # for each node, we have to trace back the path to the node before it.
        # we count the number of steps it takes to get to each node to know the edge weights
        for node in nodes:
            if node == self.end_node:
                continue

            for next_node, dist in self.get_next_nodes(node, nodes):
                self.graph.setdefault(node, []).append((next_node, dist))

        self.graph[self.end_node] = []

    def cell(self, node):
        i, j = node
        return self.grid[i][j]

    def get_next_nodes(self, node, nodes):
        result = []
        # based on the neighbors, we need to know the direction we should trace back
        # to get to the previous nodes
        up = self.check(self.up(node))
        down = self.check(self.down(node))
        left = self.check(self.left(node))
        right = self.check(self.right(node))

        if up and self.cell(up) == "^":
            result.append(self.follow(node, up, nodes))
        if down and self.cell(down) == "v":
            result.append(self.follow(node, down, nodes))
        if left and self.cell(left) == "<":
            result.append(self.follow(node, left, nodes))
        if right and self.cell(right) == ">":
            result.append(self.follow(node, right, nodes))
        if node == self.start_node and self.cell(down) == ".":
            result.append(self.follow(node, down, nodes))
        return result

    def follow(self, start, next, nodes):
        distance = 1
        path = set([start])
        current = next
        while current not in nodes:
            distance += 1
            path.add(current)
            current = self.get_next(current, path)
        return current, distance

    def check(self, node):
        i, j = node
        if 0 <= i < self.m and 0 <= j < self.n:
            return i, j

    def up(self, node):
        i, j = node
        return i - 1, j

    def down(self, node):
        i, j = node
        return i + 1, j

    def left(self, node):
        i, j = node
        return i, j - 1

    def right(self, node):
        i, j = node
        return i, j + 1

    def get_next(self, node, path):
        for i, j in self.get_neighbors(node):
            if self.grid[i][j] != "#" and (i, j) not in path:
                return i, j

    def get_neighbors(self, node):
        for f in [self.up, self.down, self.left, self.right]:
            i, j = f(node)
            if 0 <= i < self.m and 0 <= j < self.n:
                yield i, j

    def find_longest_path(self):
        distances = {node: float("-inf") for node in self.graph}
        distances[self.start_node] = 0

        for node in self.topological_sort():
            for neighbor, weight in self.graph[node]:
                if distances[neighbor] < distances[node] + weight:
                    distances[neighbor] = distances[node] + weight

        return max(distances.values())

    def topological_sort(self):
        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)

        for node in self.graph.keys():
            if node not in visited:
                dfs(node)

        return stack[::-1]


def test():
    input = get_test_input(__file__)
    g = Graph(input)
    assert g.find_longest_path() == 94


def main():
    input = get_input(__file__)
    g = Graph(input)
    print("Part 1:", g.find_longest_path())


run(main, test, ignore_other_exceptions=False)
