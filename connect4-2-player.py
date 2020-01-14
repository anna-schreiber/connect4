import numpy as np
import math
#import pygame
import sys

ROWS = 6
COLUMNS = 7
even = 0
odd = 0

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
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] and board[r][c+3]:
                return True

    # Check all vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3): # Subtract three because the last three rows don't allow for a 4 down win
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] and board[r+3][c]:
                return True

    # Check for a positive diagonal win
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3): # Subtract three because the last three rows don't allow for a 4 down win
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] and board[r+3][c+3]:
                return True

    # Check for a negative diagonal win
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS): # Start at third row
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] and board[r-3][c+3]:
                return True

board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # Get player's input
    if turn == 0:
        col = int(input("Player 1 make your selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("Player 1 wins, congrats!")
                game_over = True

    else:
        col = int(input("Player 2 make your selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("Player 2 wins, congrats!")
                game_over = True

    print_board(board)

    turn += 1
    turn = turn % 2
