rows = 6
columns = 7

piece_none = ' '
piece_red = 'r'
piece_blue = 'b'

directions = (
    (-1,-1),
    (-1,0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)

def create_board(rows = rows, columns = columns):
    board = []

    for row in range(rows):
        board_row = []
        for column in range(columns):
            board_row.append(piece_none)
        board.append(board_row)

    print_board(board)
    return board

def print_board(board):
    for row in board:
        print ('|' + '|'.join(row) + '|')

create_board(rows, columns)

# def find_winner():
