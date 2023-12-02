from functools import reduce

digits = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

digit_words = {
  'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
  'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'zero': '0'
}

def sum(lst):
  return reduce(lambda x, y: x + y, lst)

def print_result(parse, lines):
  print(sum(map(parse, lines)))

def parse_line1(line: str):
  a, *bs = filter(lambda x: x in digits, line)
  return int(''.join([a, a if len(bs) == 0 else bs[-1]]))

def parse_line2(line: str):
  index_digit_pairs = []
  for word in digit_words:
    for i, c in enumerate(line):
      digit = digit_words[word]
      if c == digit or line[i:i+len(word)] == word:
        index_digit_pairs.append((i, digit))

  a, *bs = (y for _, y in sorted(index_digit_pairs, key=lambda x: x[0]))
  return int(''.join([a, a if len(bs) == 0 else bs[-1]]))

with open('./day01.txt') as f:
  lines = f.readlines()
  print_result(parse_line1, lines)
  print_result(parse_line2, lines)
