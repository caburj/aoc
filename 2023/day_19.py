import re
from itertools import chain
from functools import reduce
from utils import get_input, get_test_input, run


CHECK_RE = re.compile(r"(\w+)([><])(\d+)")
RULE_RE = re.compile(r"(\w+)\{(.+)\}")


def parse_check(check):
    # a>123 or bb<111
    part, op, val_str = CHECK_RE.match(check).groups()
    return part, op, int(val_str)


def parse_item(line):
    vals = []
    for val in line.replace("{", "").replace("}", "").split(","):
        vals.append(int(val.split("=")[1]))
    return dict(zip("xmas", vals))


def parse_conditions(rule_content):
    conditions = []
    for condition in rule_content.split(","):
        condition = condition.strip().split(":")
        if len(condition) == 2:
            check, destination = condition
            conditions.append((parse_check(check), destination))
        else:
            conditions.append((None, condition[0]))

    return conditions


def parse_rule(line):
    name, rule_content = RULE_RE.match(line).groups()
    conditions = parse_conditions(rule_content)
    return name, conditions


def parse_input(input):
    rules_str, items_str = input.split("\n\n")
    rules = [parse_rule(line) for line in rules_str.splitlines()]
    items = [parse_item(line) for line in items_str.splitlines()]
    return dict(rules), items


def apply_rules(rules, item, start_rule_name):
    loc = start_rule_name
    while not (loc == "A" or loc == "R"):
        rule = rules[loc]
        for check, destination in rule:
            if check is None:
                loc = destination
                break
            else:
                part, op, val = check
                if op == ">":
                    if item[part] > val:
                        loc = destination
                        break
                else:
                    if item[part] < val:
                        loc = destination
                        break
        else:
            break
    return loc


def find_accepted_items(rules, items):
    accepted = []
    for item in items:
        if apply_rules(rules, item, start_rule_name="in") == "A":
            accepted.append(item)
    return accepted


def get_total_value(items):
    return sum(chain(*[item.values() for item in items]))


def get_leaf_node(value):
    return (value, lambda _: None, lambda _: None, None)


def get_node(rules, name, i, value):
    if name == "A" or name == "R":
        return (
            value,
            lambda _: get_leaf_node(name),
            lambda _: get_leaf_node(name),
            rules,
        )

    check, dest_rule = rules[name][i]
    if check is None:
        return get_node(rules, dest_rule, 0, value)
    else:
        part_type, op, val = check
        if op == ">":
            left_range = (1, val)
            right_range = (val + 1, 4000)
            left = lambda rules: get_node(rules, name, i + 1, (part_type, left_range))
            right = lambda rules: get_node(
                rules, dest_rule, 0, (part_type, right_range)
            )
            return value, left, right, rules
        else:
            left_range = (1, val - 1)
            right_range = (val, 4000)
            left = lambda rules: get_node(rules, dest_rule, 0, (part_type, left_range))
            right = lambda rules: get_node(rules, name, i + 1, (part_type, right_range))
            return value, left, right, rules


def clean_path(path):
    return tuple(path[1:-1])


def get_all_paths(rules):
    # starting from 'in' and ending in 'A' or 'R'
    root = get_node(rules, "in", 0, None)
    return set([clean_path(path) for path in find_paths(root, []) if path[-1] == "A"])


def find_paths(root, path=[]):
    if root is None:
        return []

    (node, left, right, rules) = root

    path = path + [node]

    left = left(rules)
    right = right(rules)

    # If this node is a leaf, return the current path
    if left is None and right is None:
        return [path]

    paths = []
    if left is not None:
        paths += find_paths(left, path)
    if right is not None:
        paths += find_paths(right, path)

    return paths


def get_multiplier(xs):
    if len(xs) == 0:
        return 4000

    firsts = [x[0] for x in xs]
    seconds = [x[1] for x in xs]
    return min(seconds) - max(firsts) + 1


def permute_path(path):
    return reduce(
        lambda x, y: x * y,
        [get_multiplier([r for x, r in path if x == a]) for a in ["x", "m", "a", "s"]],
    )


def test():
    input = get_test_input(__file__)
    rules, items = parse_input(input)
    assert get_total_value(find_accepted_items(rules, items)) == 19114
    assert sum([permute_path(path) for path in get_all_paths(rules)]) == 167409079868000


def main():
    input = get_input(__file__)
    rules, items = parse_input(input)
    print("Part 1:", get_total_value(find_accepted_items(rules, items)))
    print("Part 2:", sum([permute_path(path) for path in get_all_paths(rules)]))


run(main, test, ignore_other_exceptions=False)
