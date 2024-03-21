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

def is_four_in_a_row(board, row, col, dr, dc, piece):
    """
    Check if there are four consecutive pieces in the direction specified by dr and dc.
    dr, dc = -1, 0 top
    dr, dc = 1, 0 bottom
    dr, dc = 0, 1 right
    dr, dc = 0, -1 left
    dr, dc = 1, 1 bottom right
    dr, dc = -1, -1 top left
    dr, dc = 1, -1 bottom left
    dr, dc = -1, 1 top right
    """
    for _ in range(4):
        if row < 0 or row >= ROW_COUNT or col < 0 or col >= COLUMN_COUNT or board[row][col] != piece:
            return False
        row += dr
        col += dc
    return True

def winning_move(board, piece):
    # Check all directions from each position
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if is_four_in_a_row(board, row, col, 1, 0, piece) or \
                is_four_in_a_row(board, row, col, 0, 1, piece) or \
                is_four_in_a_row(board, row, col, 1, 1, piece) or \
                is_four_in_a_row(board, row, col, -1, 1, piece):
                return True
    return False

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

            if winning_move(board, 1):
                print("Player 1 wins!")
                game_over = True
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
            
            if winning_move(board, 2):
                print("AI wins!")
                game_over = True
        else:
            print("Invalid Location, please try again.")
            continue

        print_board(board)
        player = 1