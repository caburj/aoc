import re
from utils import get_test_input, get_input
from itertools import groupby

ranks = {c: i + 1 for i, c in enumerate("23456789TJQKA")}
joker_ranks = {c: i + 1 for i, c in enumerate("J23456789TQKA")}

kinds = {
    k: v + 1
    for v, k in enumerate(
        [
            "high card",
            "one pair",
            "two pairs",
            "three of a kind",
            "full house",
            "four of a kind",
            "five of a kind",
        ]
    )
}


def identify_grouped_hand(grouped_hand):
    match len(grouped_hand):
        case 5:
            return "high card"
        case 4:
            return "one pair"
        case 3:
            if len(grouped_hand[0]) == 3:
                return "three of a kind"
            else:
                return "two pairs"
        case 2:
            if len(grouped_hand[0]) == 4:
                return "four of a kind"
            else:
                return "full house"
        case 1:
            return "five of a kind"


def group_by_rank(hand):
    cards = [(c, ranks[c]) for c in hand]
    cards.sort(key=lambda x: x[1])
    cards = [c[0] for c in cards]
    groups = [list(g) for _, g in groupby(cards)]
    groups.sort(key=lambda x: len(x), reverse=True)
    return groups


def identify_hand(hand):
    return identify_grouped_hand(group_by_rank(hand))


def identify_hand_with_joker(hand):
    njokers = hand.count("J")

    if njokers == 0:
        return identify_hand(hand)

    if njokers == 5:
        return "five of a kind"

    groups = group_by_rank(hand.replace("J", ""))

    # add jokers to the strongest group
    group_1 = groups[0]
    for _ in range(njokers):
        group_1.append("J")

    return identify_grouped_hand(groups)


def read_hands(input):
    return [(x, int(y)) for x, y in [line.split(" ") for line in input.splitlines()]]


def make_sorter(ranks):
    def sorter(identified_hand):
        hand, kind, _ = identified_hand
        return (kinds[kind], *[ranks[c] for c in hand])

    return sorter


def rank_hands(hands, identifier, sorter):
    identified_hands = [(hand, identifier(hand), bet) for hand, bet in hands]
    return sorted(identified_hands, key=sorter)


def count_score(ranked_hands):
    return sum((i + 1) * bet for i, (_, _, bet) in enumerate(ranked_hands))


def get_hands_score(hands, identifier, sorter):
    return count_score(rank_hands(hands, identifier, sorter))


if __name__ == "__main__":
    test_hands = read_hands(get_test_input(__file__))
    input_hands = read_hands(get_input(__file__))

    normal_sorter = make_sorter(ranks)
    joker_sorter = make_sorter(joker_ranks)

    assert get_hands_score(test_hands, identify_hand, normal_sorter) == 6440
    print(
        "Part 1:",
        get_hands_score(input_hands, identify_hand, normal_sorter),
    )

    assert get_hands_score(test_hands, identify_hand_with_joker, joker_sorter) == 5905
    print(
        "Part 2:",
        get_hands_score(input_hands, identify_hand_with_joker, joker_sorter),
    )
