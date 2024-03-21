import numpy as np
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    if(col >= 0 and col < 7):
        return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

board = create_board()
print_board(board)
game_over = False
player = 0

while not game_over:
    if player == 1:
        col = int(input("Player 1 make your selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
        else:
            print("Invalid Location, please try again.")
            continue

        print_board(board)
        player = 0
    else:
        col = int(input("Player 2 make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
        else:
            print("Invalid Location, please try again.")
            continue

        print_board(board)
        player = 1