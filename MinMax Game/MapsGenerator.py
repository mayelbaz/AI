import operator
import numpy as np

def tup_add(t1, t2):
    return tuple(map(operator.add, t1, t2))

def tup_num_mul(t1, i):
    return tuple([x * i for x in t1])

def square(size, left_down_corner):
    blocks = []
    for i in range(size):
        for j in range(size):
            blocks.append(tup_add(left_down_corner, (i, j)))
    return blocks

def tunnel(length, direction, left_down_corner, space=1):
    if direction == 'horizontal':
        direction = (0, 1)
        hist = (1 + space, 0)
    else:
        assert direction == 'vertical'
        direction = (1, 0)
        hist = (0, 1 + space)

    blocks = []
    for i in range(length):
        loc = tup_add(left_down_corner, tup_num_mul(direction, i))
        blocks.append(loc)
        blocks.append(tup_add(loc, hist))
    return blocks

def reflect(board, direction):
    if direction == 'vertical':
        board = np.transpose(board)
    reflection = np.fliplr(board)
    new_board = []
    for row , reflected_row in zip(board, reflection):
        new_row = list(row) + list(reflected_row)
        new_board.append(new_row)
    if direction == 'vertical':
        new_board = np.transpose(new_board)
    return new_board

def build_board(size, blocks, starts):
    board = np.zeros(size)
    for i, j in blocks:
        board[i][j] = -1

    for player_index, (i, j) in enumerate(starts):
            board[i][j] = player_index + 1
    return board

def get_board_data(board):
    size = len(board), len(board[0])
    blocks = []
    starts = [None, None]
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == -1:
                blocks.append((i, j))
            elif val > 0:
                blocks[val - 1] = (i, j)
    return size, blocks, starts

# Creating Maps
n = 9
m = 10
size = (n, m)
blocks = []
for i in range(1, 7, 4):
    for j in range(1, 9, 3):
        direction = 'horizontal'
        blocks += (tunnel(2, direction, (i, j)))
starts = [(0, 0), (8, 9)]

tunnels_map = [size, blocks, starts]

blocks = []
for i in range(4):
    blocks.append((i, i))
    blocks.append((i, i+3))


n = max([x[0] for x in blocks]) + 2
m = max([x[1] for x in blocks]) + 2
size = (n, m)
board = build_board(size, blocks, [])
board = reflect(board, 'horizontal')
size, blocks, _ = get_board_data(board)
starts = [(0, 7), (0, 8)]

diag_map = [size, blocks, starts]

squares_locations = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (7, 9), (6, 10), (5, 11), (4, 12),
                     (3, 13), (2, 14), (1, 15),
                     (3, 5), (3, 7), (3, 9), (3, 11),
                     (1, 16), (1, 18), (1, 20),
                     (3, 18), (5, 18), (7, 18), (8, 18),
                     (8, 16), (8, 18), (8, 20)]


blocks = sum([square(2, x) for x in squares_locations], [])
n = max([x[0] for x in blocks]) + 1
m = max([x[1] for x in blocks]) + 1
size = (n, m)
board = build_board(size, blocks, [])
board = reflect(board, 'horizontal')
board = reflect(board, 'vertical')

for i, row in enumerate(board):
    for j, val in enumerate(row):
        if (i > 9 and j <= 21) or (i <= 9 and j > 21):
            board[i][j] = -(1 - (-val))

size, blocks, _ = get_board_data(board)
blocks.remove((0, 22))
blocks.remove((19, 21))
blocks.remove((9, 28))
blocks.remove((10, 15))
for i in range(10):
    blocks.remove((10 + i, 0))
    blocks.remove((i, size[1] - 1))

starts = [(0, 0), (size[0] - 1, size[1] - 1)]

ai_map = [size, blocks, starts]
ai_board = build_board(size, blocks, starts)

#########################

board = \
[
    [-1,  0,  0,  0,  0, -1, -1, -1, -1],
    [ 0, -1, -1,  0,  0, -1,  0,  0, -1],
    [ 0, -1,  0, -1,  0, -1,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0, -1, -1],
    [-1, -1,  -1, 0, -1,  0,  0,  0, -1],
    [ 0,  0,  0,  0,  0,  0,  0,  0, -1],
 ]

board = reflect(board, 'horizontal')
size, blocks, _ = get_board_data(board)
starts = [(2, 2), (2, 15)]
trick_map = [size, blocks, starts]
#########################

board = \
[
    [ 0,  0,  0],
    [ 0,  0,  0],
    [ 0,  0,  0],
    [ 0,  0, -1],
    [ 0,  0, -1],
    [ 0,  0, -1],
 ]

board = reflect(board, 'horizontal')
size, blocks, _ = get_board_data(board)
starts = [(4, 1), (4, 4)]
small_map = [size, blocks, starts]

maps = [small_map, diag_map, tunnels_map, trick_map, ai_map]