from math import floor
from random import randint
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

# GENERATE BOARD


def shift_square_down(square, n=1):
  _square = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  for i in range(9):
    _i = i - (3 * n)
    _i %= 9
    _square[i] = square[_i]
  return _square


def shift_square_right(square, n=1):
  _square = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  for i in range(9):
    _i = ((i % 3) - n) % 3 + (i // 3) * 3
    _square[i] = square[_i]
  return _square


def shift_board_squares_down(board, n=1):
  _board = board.copy()
  for i in range(9):
    _board[i] = shift_square_down(_board[i], n)
  return _board


def shift_board_squares_right(board, n=1):
  _board = board.copy()
  for i in range(9):
    _board[i] = shift_square_right(_board[i], n)
  return _board


def shift_board(board, x_shift=0, y_shift=0):
  _board = board.copy()

  for i in range(9):
    x, y = convert_ij_to_xy(0, i)
    x = (x - x_shift) % 3
    y = (y - y_shift) % 3
    _, _i = convert_xy_to_ij(x, y)
    _board[_i] = board[i]

  return _board


def generate_board(board):
  _board = board.copy()
  for i in range(9):
    for j in range(9):
      _board[i][j] = j + 1

  for i in range(9):
    down_shifts = i % 3
    right_shifts = i // 3
    _board[i] = shift_square_down(_board[i], down_shifts)
    _board[i] = shift_square_right(_board[i], right_shifts)

  _board = shift_board_squares_down(_board, randint(0, 2))
  _board = shift_board_squares_right(_board, randint(0, 2))
  _board = shift_board(_board, randint(0, 3), randint(0, 2))

  # TODO: add logic here for one unique solution
  #       (makes it possible for automatic_board()
  #       to solve the board)
  # TODO: confirm the above claim
  n = randint(0, 9)
  for i in range(9):
    for j in range(9):
      if get_board_ij(_board, i, j) == n:
        _board[i][j] = 0
  n = randint(0, 9)
  for i in range(9):
    for j in range(9):
      if get_board_ij(_board, i, j) == n:
        _board[i][j] = 0

  return _board


def validate_board(board):
  for i in range(9):
    for j in range(9):
      for n in range(9):
        check = check_sector(board, i, j, n + 1)
        if check != 'pass':
          return False
  return True


# AUTOMATIC BOARD


# TODO: add row and column checks
def automatic_board(board):
  _board = board.copy()

  changed = False

  for n in range(1, 10):
    # square checks
    for i in range(9):
      square = _board[i]
      if square.count(0) != 1:
        continue
      if n in square:
        continue
      j = square.index(0)
      check = check_sector(_board, i, j, n, strict=True)
      if check == 'pass':
        set_board_ij(_board, i, j, n)
        changed = True

    # row checks
    for y in range(9):
      row = get_board_row_xy(_board, y)
      if row.count(0) != 1:
        continue
      if n in row:
        continue
      x = row.index(0)
      i, j = convert_xy_to_ij(x, y)
      check = check_sector(_board, i, j, n, strict=True)
      if check == 'pass':
        set_board_ij(_board, i, j, n)
        changed = True

    # column checks
    for x in range(9):
      column = get_board_column_xy(_board, x)
      if column.count(0) != 1:
        continue
      if n in column:
        continue
      y = column.index(0)
      i, j = convert_xy_to_ij(x, y)
      check = check_sector(_board, i, j, n, strict=True)
      if check == 'pass':
        set_board_ij(_board, i, j, n)
        changed = True

  if not changed:
    # _board = automatic_board_free(_board)
    # TODO: implement algorimic solution
    open = get_board_matches_ij(_board, 0)
    open_options = {}
    
    for open_cell in open:
      options = get_valid_options_ij(_board, open_cell[0], open_cell[1])
      open_options[open_cell] = options

    unique_options = []
    for _, options in open_options:
      for option in options:
        if option not in unique_options:
          unique_options.append(option)

    print(unique_options)
    sleep(5)

  return _board


def automatic_board_free(board):
  _board = board.copy()
  for n in range(1, 10):
    for i in range(9):
      for j in range(9):
        if _board[i][j] != 0:
          continue
        check = check_sector(_board, i, j, n, strict=True)
        if check == 'pass':
          set_board_ij(_board, i, j, n)
  return _board


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


def get_board_row_xy(board, y):
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


def get_board_column_xy(board, x):
  column = []
  for y in range(0, 9):
    column.append(get_board_xy(board, x, y))
  return column


def get_letter(number):
  letter = '?'

  if number == 0:
    letter = ' '
  elif number < 0:
    letter = f'\033[31m{str(number)[1]}'
  elif number > 0:
    letter = f'{number}'

  return letter


def make_board_row():
  board = make_board()
  for x in range(9):
    set_board_xy(board, x, 0, x + 1)
  return board


def make_board_column():
  board = make_board()
  for y in range(9):
    set_board_xy(board, 0, y, y + 1)
  return board


def get_board_matches_ij(board, n):
  open = []
  for i in range(9):
    for j in range(9):
      if get_board_ij(board, i, j) == n:
        open.append((i, j))
  return open


def get_valid_options_ij(board, i, j):
  options = []
  for n in range(1, 10):
    check = check_sector(board, i, j, n, strict=True)
    if check == 'pass':
      options.append(n)
  return options


# MAIN BOARD FUNCTIONS


def make_board():
  return [[0 for _ in range(9)] for _ in range(9)]


def print_board(board, error_square=None, error_row=None, error_column=None):
  for y in range(9):
    for x in range(9):
      i, j = convert_xy_to_ij(x, y)
      color = '\033[47m' if i % 2 == 0 else '\033[0m'
      number = get_board_ij(board, i, j)
      letter = get_letter(number)

      red_bg = '\033[41m'
      if error_square is not None and i == error_square:
        color += red_bg
      if error_row is not None and y == error_row:
        color += red_bg
      if error_column is not None and x == error_column:
        color += red_bg

      print(end=f'{color}{letter} \033[0m')
    print()


def check_sector(board, i, j, n, strict=False):
  _board = board.copy()

  square = get_board_square_i(_board, i)
  if square.count(n) > 1 or (strict and square.count(n) != 0):
    return 'fail: square'

  row = get_board_row_ij(_board, i, j)
  if row.count(n) > 1 or (strict and row.count(n) != 0):
    return 'fail: row'

  column = get_board_column_ij(_board, i, j)
  if column.count(n) > 1 or (strict and column.count(n) != 0):
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
  print()
  sleep(0.5)


def handle_user(user, board):
  if user == 'up':
    return shift_board_squares_down(board, n=-1)

  if user == 'down':
    return shift_board_squares_down(board)

  if user == 'right':
    return shift_board_squares_right(board)

  if user == 'left':
    return shift_board_squares_right(board, n=-1)

  if user == 'auto':
    return automatic_board(board)

  if user == 'auto free':
    return automatic_board_free(board)

  if user == 'regenerate':
    return generate_board(board)

  if user == 'clear':
    return make_board()

  if user == 'test row':
    return make_board_row()

  if user == 'test column':
    return make_board_column()

  if user == 'validate':
    validation = validate_board(board)
    message = 'valid' if validation else 'invalid'
    print(f'\033[A\r{message}{" " * 20}\r')
    sleep(0.5)
    return board

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
  if n < -9 or n > 9:
    return board

  check = check_sector(board, i, j, n)
  if n > 0 and check != "pass":
    check_fail(board, i, j, check)
    return board

  return set_board_ij(board, i, j, n)


def clear():
  string = f'\033[A\r{" " * 20}\r' * 10
  print(end=string)


board = make_board()
board = generate_board(board)
user = ""
while user != 'done':
  print_board(board)
  user = input(">> ")
  board = handle_user(user, board)
  clear()
