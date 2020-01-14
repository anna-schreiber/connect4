import numpy as np
import math
#import pygame
import sys
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

WINDOW_LENGTH = 4

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

def evaluate_score(window, piece):
    score = 0
    
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
        
    if window.count(piece) == 4:
            score += 100 # Gives a score of 100 for 4-in-a-row
    elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10 # Gives a score of 10 for 3-in-a-row
    elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5 # Gives a score of 10 for 3-in-a-row

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 80

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:,COLUMNS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6 # Give higher scores for pieces places in the center of the board
    
    # Score horizontal locations
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])] # Create an array that contains the first four items of a that row
        for c in range(COLUMNS - 3): # Don't include the last 3 columns, because a 4-in-a-row can't start from col 4
            window = row_array[c:c+WINDOW_LENGTH] # Process this array 4 spots at a time
            score += evaluate_score(window, piece)

    # Score vertical locations
    for c in range(COLUMNS):
        column_array = [int(i) for i in list(board[:,c])] # Create an array that contains the first four items of a that column
        for r in range(ROWS - 3): # Don't include the last 3 rows, because a 4-in-a-row can't start from row 3
            window = column_array[r:r+WINDOW_LENGTH] # Process this array 4 spots at a time
            score += evaluate_score(window, piece)

    # score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_score(window, piece)

    # score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_score(window, piece)

    return score

def get_valid_locations(board):
    valid_locations = [] # Initialize empty list of valid locations
    for col in range(COLUMNS):
        if is_valid_location(board, col): # Check all valid locations
            valid_locations.append(col) # If the spot is valid, append it to the valid_locations list
    return valid_locations

def pick_best_move(board, piece):
    best_score = -10000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col) 
        temp_board= board.copy() # Creates a copy of our game board in a different memory location
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, CPU) # Randomly selects who goes first

while not game_over:
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

        col = pick_best_move(board, CPU_PIECE)
        
        # col = random.randint(0, COLUMNS-1) # Pick a random column to drop a piece in
        
        if is_valid_location(board, col):
            time.sleep(2) # Delay computer's turn 2 seconds
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, CPU_PIECE)

            if winning_move(board, CPU_PIECE):
                print("Computron wins, beep boop")
                game_over = True

            turn += 1
            turn = turn % 2

    print_board(board)


    
