import numpy as np
import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
TREE_DEPTH = 4

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WIN = False

WINDOW_LENGTH = 4

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
    char_board = np.where(board==1, 'X', board)
    char_board = np.where(char_board=='2.0', 'O', char_board)
    char_board = np.where(char_board=='0.0', ' ', char_board)
    print(np.flip(char_board, 0))

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
            if is_four_in_a_row(board, row, col, 1, 0, piece) or is_four_in_a_row(board, row, col, 0, 1, piece) or is_four_in_a_row(board, row, col, 1, 1, piece) or is_four_in_a_row(board, row, col, -1, 1, piece):
                return True
    return False

def evaluate_board(window, piece):
    score = 0
    opp_piece = AI_PIECE if piece == PLAYER_PIECE else PLAYER_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4
    
    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_board(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_board(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_board(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_board(window, piece)

    return score

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_location = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                    return (None, math.inf)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

board = create_board()
print_board(board)

game_over = False
turn = random.randint(PLAYER, AI)

while not game_over:
    if turn == PLAYER:
        while True:
            try:
                if is_terminal_node(board):
                    break
                col = int(input("Player 1 make your selection (0-6): "))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, 1):
                        print("Player 1 wins!")
                        game_over = True
                        WIN = True
                        break

                    turn += 1
                    turn = turn % 2
                    break
                else:
                    print("Invalid input, please enter a number between 0 and 6.")
            except ValueError:
                print("Invalid input, please enter a number between 0 and 6.")

    else:
        while True:
            if is_terminal_node(board):
                game_over = True
                break
            
            col = minimax(board, 5, -math.inf, math.inf, True)[0]
            print(col)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            
            if winning_move(board, AI_PIECE):
                print("AI2 wins!")
                game_over = True
                WIN = True
                break
            
            print("\n\nAI2's move:")
            print_board(board)
            turn += 1
            turn = turn % 2
            break

print_board(board)
if not WIN:
    print("It's a tie!")