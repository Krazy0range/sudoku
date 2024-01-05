from math import floor
from time import sleep

# i:
# 0 0 0  1 1 1  2 2 2
# 0 0 0  1 1 1  2 2 2
# 0 0 0  1 1 1  2 2 2
# 3 3 3  4 4 4  5 5 5
# 3 3 3  4 4 4  5 5 5
# 3 3 3  4 4 4  5 5 5
# 6 6 6  7 7 7  8 8 8
# 6 6 6  7 7 7  8 8 8
# 6 6 6  7 7 7  8 8 8

# j:
# 0 1 2
# 3 4 5
# 6 7 8

# xy:
# 00 10 20  30 40 50  60 70 80
# 01 11 21  31 41 51  61 71 81
# 02 12 22  32 42 52  62 72 82
# 03 13 23  33 43 53  63 73 83
# 04 14 24  34 44 54  64 74 84
# 05 15 25  35 45 55  65 75 85
# 06 16 26  36 46 56  66 76 86
# 07 17 27  37 47 57  67 77 87
# 08 18 28  38 48 58  68 78 88

# i = floor(x / 3) + (floor(y / 3) * 3)
# j = x % 3 + ((y % 3) * 3)

# HELPER BOARD FUNCTIONS

def set_board_ij(board, i, j, n):
  _board = board.copy()
  _board[i][j] = n
  return _board

def set_board_xy(board, x, y, n):
  i, j = convert_xy_to_ij(x, y)
  return set_board_ij(board, i, j, n)

def get_board_ij(board, i, j):
  return board[i][j]

def convert_xy_to_ij(x, y):
  i = floor(x / 3) + (floor(y / 3) * 3)
  j = x % 3 + ((y % 3) * 3)
  return (i, j)

def convert_ij_to_xy(i, j):
  x = j % 3 + ((i % 3) * 3)
  y = floor(j / 3) + (floor(i / 3) * 3)
  return (x, y)

def get_board_xy(board, x, y):
  i, j = convert_xy_to_ij(x, y)
  return get_board_ij(board, i, j)

def get_board_square_i(board, i):
  return board[i]

def get_board_row_ij(board, i, j):
  _, y = convert_ij_to_xy(i, j)
  row = []
  for x in range(0, 9):
    row.append(get_board_xy(board, x, y))
  return row

def get_board_column_ij(board, i, j):
  x, _ = convert_ij_to_xy(i, j)
  column = []
  for y in range(0, 9):
    column.append(get_board_xy(board, x, y))
  return column

def get_letter(number):
  letter = '-'
  
  if number == -9:
    letter = ' '
  elif number < 0:
    letter = f'\033[31m{str(number)[1]}'
  elif number > 0:
    letter = f'{number}'
    
  return letter

# MAIN BOARD FUNCTIONS

def make_board():
  return [[-9 for _ in range(9)] for _ in range(9)]

def print_board(board, error_square = None, error_row = None, error_column = None):
  for y in range(9):
    for x in range(9):
      i, j = convert_xy_to_ij(x, y)
      color = '\033[47m' if i % 2 == 0 else '\033[0m'
      number = get_board_ij(board, i, j)
      letter = get_letter(number)
      
      red_bg = '\033[41m'
      if error_square is not None:
        if i == error_square:
          color += red_bg
      if error_row is not None:
        if y == error_row:
          color += red_bg
      if error_column is not None:
        if x == error_column:
          color += red_bg
      
      print(end=f'{color}{letter} \033[0m')
    print()

def check_board(board, i, j, n):
  _board = board.copy()
  
  square = get_board_square_i(_board, i)
  if n in square:
    return 'fail: square'

  row = get_board_row_ij(_board, i, j)
  if n in row:
    return 'fail: row'
  
  column = get_board_column_ij(_board, i, j)
  if n in column:
    return 'fail: column'
  
  return 'pass'

def check_fail(board, i, j, check):
  error_square = None
  error_row = None
  error_column = None
  if 'square' in check:
    error_square = i
  if 'row' in check:
    error_row = convert_ij_to_xy(i, j)[1]
  if 'column' in check:
    error_column = convert_ij_to_xy(i, j)[0]

  clear()
  print_board(board, error_square, error_row, error_column)
  sleep(0.5)
  clear()

def handle_user(user, board):
  numbers = user.split()
  
  if len(numbers) != 3:
    return board

  try:
    i = int(numbers[0])
    j = int(numbers[1])
    n = int(numbers[2])
  except ValueError:
    return board

  if i < 0 or i > 8: 
    return board
  if j < 0 or j > 8:
    return board
  if n < -9 or n > 8:
    return board

  check = check_board(board, i, j, n)
  if n > 0 and not check == "pass":
    check_fail(board, i, j, check)
    return board

  return set_board_ij(board, i, j, n)

def clear():
  string = f'\033[A\r{" " * 20}\r' * 10
  print(end=string)

board = make_board()
user = ""
while not user == "done":
  print_board(board)
  user = input(">> ")
  board = handle_user(user, board)
  clear()