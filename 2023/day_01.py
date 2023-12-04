from utils import get_input_str


digit_words = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
}


def make_int(digits: list[str]):
    assert len(digits) > 0
    return int(digits[0] + digits[-1])


def parse_line1(line: str):
    digits_found = [x for x in line if x in digit_words.values()]
    return make_int(digits_found)


def parse_line2(line: str):
    digits_found = []
    for i, c in enumerate(line):
        for word in digit_words:
            digit = digit_words[word]
            if c == digit or line[i : i + len(word)] == word:
                digits_found.append(digit)

    return make_int(digits_found)


input_str = get_input_str(__file__)
lines = input_str.splitlines()
print("Part 1:", sum(map(parse_line1, lines)))
print("Part 2:", sum(map(parse_line2, lines)))
