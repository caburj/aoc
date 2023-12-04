import re

space_re = re.compile(r"\s+")


def get_winning_number_count(numbers_str):
    winning_str, entry_str = numbers_str.strip().split("|")
    winning = {int(x) for x in re.split(space_re, winning_str.strip())}
    entry = {int(x) for x in re.split(space_re, entry_str.strip())}
    return len(winning.intersection(entry))


def compute_score(line):
    _, numbers_str = line.split(":")
    count = get_winning_number_count(numbers_str)
    if count == 0:
        return 0
    return pow(2, count - 1)


with open("2023/04/input.txt") as f:
    lines = f.readlines()
    print("Part 1:", sum(compute_score(line) for line in lines))

    # Part 2: Win the next cards based on number of matches.
    counts = {i + 1: 1 for i in range(len(lines))}
    for card_id in counts:
        line = lines[card_id - 1]
        _, numbers = line.split(":")
        num_won_cards = counts[card_id]
        for j in range(card_id, card_id + get_winning_number_count(numbers)):
            dest = j + 1
            if dest in counts:
                counts[dest] += num_won_cards

    print("Part 2:", sum(counts.values()))
