def parse_line(line: str):
  game_name, game = line.split(':')
  cubes = []
  for col in game.strip().split(';'):
    colors = col.strip().split(',')
    for color in colors:
      num_str, color = color.strip().split(' ')
      num = int(num_str.strip())
      cubes.append((num, color.strip()))

  game_id = int(game_name.strip().split(' ')[1])
  return (game_id, cubes)

def is_possible(max_cubes, subset_cubes):
  for num, cube in subset_cubes:
    max_cube = max_cubes[cube]
    if num > max_cube:
      return False

  return True

def min_possible(game_cubes):
  min_cubes = {'red': 0, 'green': 0, 'blue': 0}
  for num, cube in game_cubes:
    if min_cubes[cube] < num:
      min_cubes[cube] = num

  return min_cubes

def cube_product(min_cubes):
  return min_cubes['red'] * min_cubes['green'] * min_cubes['blue']


with open('2023/day02.txt') as f:
  lines = f.readlines()
  games = list(map(parse_line, lines))
  max_cubes = {'red': 12, 'green': 13, 'blue': 14}
  possible_games = [game_id for game_id, cubes in games if is_possible(max_cubes, cubes)]
  print('Part 1:', sum(possible_games))
  all_min_cubes = list(map(min_possible, map(lambda x: x[1], games)))
  print('Part 2:', sum(map(cube_product, all_min_cubes)))
