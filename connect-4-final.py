## Play against bot (basic game logic) or trained AI (ML/RL/minimax)

import json
import requests
import numpy as np
import math
import random

ROWS = 6
COLUMNS = 7

# Used to randomly determine which player goes first
PLAYER = 0
CPU = 1

# Currently the pieces are 1 and 2, could be changed to red and yellow
PLAYER_PIECE = 1
CPU_PIECE = 2

# When the game starts, this triggers the option to play against a bot or AI
MOVE = 0

WIN_COLUMN = 0

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0 # Check to see if the column has an open spot

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r # Return first open spot in a given column

def print_board(board):
    print(np.flip(board, 0)) # Flips the board 180 degrees

def winning_move(board, piece):
    # Check all horizontal locations for win
    for c in range(COLUMNS - 3): # Subtract three because the last three columns don't allow for a 4 across win
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check all vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3): # Subtract three because the last three rows don't allow for a 4 down win
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check for a positive diagonal win
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3): # Subtract three because the last three rows don't allow for a 4 down win
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check for a negative diagonal win
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS): # Start at third row
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def api_alg(board):
    json_board = json.dumps(board.tolist())
    #url = "http://127.0.0.1:5000/api/v1/movealg"
    url = "https://tnx10c81ea.execute-api.us-east-1.amazonaws.com/dev/movealg"
    data = {
        "board": json_board
    }
    r = requests.post(url, json=data)
    col_number = int(r.json())
    return col_number

def api_minimax(board, depth):
    json_board = json.dumps(board.tolist())
    #url = "http://127.0.0.1:5000/api/v1/moveminimax"
    url = "https://rsnva5xewi.execute-api.us-east-1.amazonaws.com/dev"
    headers = {
        "x-api-key": "KlHMsZdpjaaQ6sfFKIuhy1jyPCvBKArd4dOj3vQa"
    }
    data = {
        "board": json_board, 
        "depth": depth, 
        #"maximizingPlayer": maximizingPlayer, 
        "num_columns": COLUMNS, 
        "cpu_piece": CPU_PIECE, 
        "player_piece":PLAYER_PIECE,
        "num_rows": ROWS, 
        "window_length": WINDOW_LENGTH
        }
    r = requests.post(url, json=data, headers=headers)
    col_number = int(r.json())
    return col_number

board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, CPU) # Randomly selects who goes first

while not game_over:
    if MOVE == 0:
        game_version = int(input("Would you like to play against a beginner bot or expert AI? Enter 0 for bot, 1 for AI: "))
        MOVE = 1
    # Get player's input
    if turn == PLAYER:
        col = int(input("Player 1 make your selection (0-6): "))

        if is_valid_location(board, col): # Check if selected column is valid
            row = get_next_open_row(board, col) # Find the first available spot in that column
            drop_piece(board, row, col, PLAYER_PIECE) # Drop piece in the spot

            if winning_move(board, PLAYER_PIECE):
                print("Player 1 wins, congrats!")
                game_over = True

            turn += 1
            turn = turn % 2

    # Computer's turn
    if turn == CPU and not game_over:
        print("Computron is thinking...")

        if game_version == 0:
            col = api_alg(board)
        else:
            col = api_minimax(board, 4)
                
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, CPU_PIECE)

            if winning_move(board, CPU_PIECE):
                print("Computron wins, beep boop")
                game_over = True

            turn += 1
            turn = turn % 2

    print_board(board)


    
