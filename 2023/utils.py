from functools import reduce

def sum(lst):
  return reduce(lambda x, y: x + y, lst)
