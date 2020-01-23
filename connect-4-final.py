## Play against bot (basic game logic) or trained AI (ML/RL/minimax)

import json
import requests
import numpy as np
import math
import random
import time

ROWS = 6
COLUMNS = 7
even = 0
odd = 0

PLAYER = 0
CPU = 1

PLAYER_PIECE = 1
CPU_PIECE = 2

MOVE = 0

WINDOW_LENGTH = 4

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

def check_window(window, piece):
    position = 0
    
            
    if window.count(piece) == 3 and window.count(0) == 1:
        print(window)
        for i in window:
            if window[int(i)] == 0:
                print(int(i))
                position = int(i)
        move_win = True
    else:
        move_win = False

    # if window.count(opponent_piece) == 3 and window.count(0) == 1:
    #     move_block = True
    # else:
    #     move_block = False
    #print(move_win, position)
    return move_win, position #, move_block

def evaluate_position(board, piece):
    global WIN_COLUMN
    win_opportunity = False
    block_opportunity = False
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = CPU_PIECE

    # Check for three in a row horizontal locations
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])] # Create an array that contains the first four items of a that row
        for c in range(COLUMNS - 3): # Don't include the last 3 columns, because a 4-in-a-row can't start from col 4
            window = row_array[c:c+WINDOW_LENGTH] # Process this array 4 spots at a time
            if window.count(piece) == 3 and window.count(0) == 1:
                win_opportunity = True
                for i in range(WINDOW_LENGTH):
                    if window[i] == 0:
                        WIN_COLUMN = i + c
            if window.count(opponent_piece) == 3 and window.count(0) == 1:
                print("block horizontal win")

    # Score vertical locations
    for c in range(COLUMNS):
        column_array = [int(i) for i in list(board[:,c])] # Create an array that contains the first four items of a that column
        for r in range(ROWS - 3): # Don't include the last 3 rows, because a 4-in-a-row can't start from row 3
            window = column_array[r:r+WINDOW_LENGTH] # Process this array 4 spots at a time
            if window.count(piece) == 3 and window.count(0) == 1:
                win_opportunity = True
                WIN_COLUMN = c
            if window.count(opponent_piece) == 3 and window.count(0) == 1:
                print("block vertical win")
                block_opportunity = True
                WIN_COLUMN = c

    # score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            if window.count(piece) == 3 and window.count(0) == 1:
                win_opportunity = True
                for i in range(WINDOW_LENGTH):
                    if window[i] == 0:
                        WIN_COLUMN = i + c
            if window.count(opponent_piece) == 3 and window.count(0) == 1:
                print("block pos diagonal win")

    # score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            win_move = check_window(window, piece)
            if window.count(piece) == 3 and window.count(0) == 1:
                win_opportunity = True
                for i in range(len(window)):
                    if window[i] == 0:
                        WIN_COLUMN = i + c
            if window.count(opponent_piece) == 3 and window.count(0) == 1:
                print("block neg diagonal win")
    
    #print(WIN_COLUMN)
    return win_opportunity, block_opportunity

def get_valid_locations(board):
    valid_locations = [] # Initialize empty list of valid locations
    for col in range(COLUMNS):
        if is_valid_location(board, col): # Check all valid locations
            valid_locations.append(col) # If the spot is valid, append it to the valid_locations list
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col) 
        #temp_board= board.copy() # Creates a copy of our game board in a different memory location
        #drop_piece(temp_board, row, col, piece)
        win_move, block_move = evaluate_position(board, piece)
        #print(win_move)
        #print(win_move, col)
        if win_move:
            #print(WIN_COLUMN)
            best_col = WIN_COLUMN
        if block_move:
            best_col = WIN_COLUMN
            #print(win_move, best_col)
    return best_col

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

def api_alg(COLUMNS):
    url = "http://127.0.0.1:5000/api/v1/movealg"
    #url = "https://tnx10c81ea.execute-api.us-east-1.amazonaws.com/dev/movealg"
    data = {"num_columns": COLUMNS}
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
        #"num_columns": COLUMNS, 
        "num_rows": ROWS, 
        "window_length": WINDOW_LENGTH
        }
    r = requests.post(url, json=data, headers=headers)
    col_number = int(r.json())
    return col_number

# def api_ml(board, piece):
#     json_board = json.dumps(board.tolist())
#     url = "http://127.0.0.1:5000/api/v1/moveml"
#     data = {
#         "board": json_board, 
#         "cpu_piece": piece, 
#         "player_piece":PLAYER_PIECE, 
#         "num_columns": COLUMNS, 
#         "num_rows": ROWS, 
#         "window_length": WINDOW_LENGTH
#         }
#     r = requests.post(url, json=data)
#     col_number = int(r.json())
#     return col_number

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
            col = pick_best_move(board, CPU_PIECE)
            # TODO make basic logic version
            #col = api_alg(COLUMNS)
            #col, minimax_score = minimax(board, 1, True)
        else:
            col = api_minimax(board, 4)
            #col = api_ml(board, CPU_PIECE)
            #col = pick_best_move(board, CPU_PIECE)
                
        if is_valid_location(board, col):
            #time.sleep(2) # Delay computer's turn 2 seconds
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, CPU_PIECE)

            if winning_move(board, CPU_PIECE):
                print("Computron wins, beep boop")
                game_over = True

            turn += 1
            turn = turn % 2

    print_board(board)


    
