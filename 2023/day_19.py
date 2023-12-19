import re
from itertools import chain
from utils import get_input, get_test_input, run


CHECK_RE = re.compile(r"(\w+)([><])(\d+)")


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
    rule_re = re.compile(r"(\w+)\{(.+)\}")
    name, rule_content = rule_re.match(line).groups()
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


def test():
    input = get_test_input(__file__)
    rules, items = parse_input(input)
    assert get_total_value(find_accepted_items(rules, items)) == 19114


def main():
    input = get_input(__file__)
    rules, items = parse_input(input)
    print('Part 1:', get_total_value(find_accepted_items(rules, items)))



run(main, test, ignore_other_exceptions=False)
