import numpy as np
import random
import colors_for_the_game as c
import tkinter as tk

NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])


def initialize_game():
    board = np.zeros(16, dtype="int")
    # Return a new array of given shape and type,
    # filled with zeros and two random of two cells with values of 2.
    # Random selection of two indexes to place a
    # starting value of 2 in 2 cells
    board = board.reshape((4, 4))  # creating a matrix of 4X4
    row_1 = random.randint(0, 3)
    col_1 = random.randint(0, 3)
    board[row_1][col_1] = 2
    row_2 = random.randint(0, 3)
    col_2 = random.randint(0, 3)
    if not (row_2 == row_1 and col_2 == col_1):
        board[row_2][col_2] = 2
    else:  # in case that both tile in same place
        flag = True  # same row and col
        while flag:
            row_2 = random.randint(0, 3)
            col_2 = random.randint(0, 3)
            if not (row_2 == row_1 and col_2 == col_1):
                board[row_2][col_2] = 2
                flag = False
    return board


def push_board_right(board):
    # This function manipulate the the board to move right by "pushing it".
    # The function create new board that was
    # pushed right. The function returns new board (matrix) that pushed right (without merging cells),
    # and if the function done it propose it will return true or else false.
    new = np.zeros((4, 4), dtype="int")
    done = False
    for row in range(4):
        count = 4 - 1
        for col in range(4 - 1, -1, -1):
            if board[row][col] != 0:
                new[row][count] = board[row][col]
                if col != count:
                    done = True
                count -= 1
    return new, done


def merge_elements(board):
    # This function merge 2 cells with the the value and turns to be a new merge value that is
    # (same value + same value)
    # for an Example: two cells of 2 becomes a merge cell of 4 The function returns the latest board that
    # values in it merged, the score of the player when he merge the cells, and if the function done it propose.
    score = 0
    done = False
    for row in range(4):
        for col in range(4 - 1, 0, -1):
            if board[row][col] == board[row][col - 1] and board[row][col] != 0:
                board[row][col] *= 2
                score += board[row][col]
                board[row][col - 1] = 0
                done = True
    return board, done, score


def move_up(board):
    # This function manipulate the the board to move up by the "Up key",
    # the function create new latest board that
    # was pushed up by player choice (or the Bot choice) like in real 2048 game.
    # The function returns new board (matrix) that moved up, if the move is made, and the score.
    rotated_board = np.rot90(board, -1)  # ---> rotate the board by 90 degree of the matrix
    pushed_board, has_pushed = push_board_right(rotated_board)
    merged_board, has_merged, score = merge_elements(pushed_board)
    second_pushed_board, second_pushed_made = push_board_right(merged_board)
    rotated_back_board = np.rot90(second_pushed_board)  # rotate the board by 90 degree of the matrix in opposite
    # direction
    move_made = has_pushed or has_merged
    return rotated_back_board, move_made, score


def move_down(board):
    # This function manipulate the the board to move down by the "Down key",
    # the function create new latest board that
    # was pushed down by player choice (or the Bot choice) like in real 2048 game.
    # The function returns the latest board (matrix) that moved down, if the move is made, and the score.
    board = np.rot90(board)  # ---> rotate the board by 90 degree of the matrix
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, second_pushed_made = push_board_right(board)
    board = np.rot90(board, -1)  # ---> rotate the board by 90 degree of the matrix in opposite direction
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_left(board):
    # This function manipulate the the board to move left by the "Left key",
    # the function create new latest board that
    # was pushed left by player choice (or the Bot choice) like in real 2048 game.
    # The function returns the latest board (matrix) that moved left, if the move is made, and the score.
    board = np.rot90(board, 2)  # ---> rotate the board by 90 degree of the matrix
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, second_pushed_made = push_board_right(board)
    board = np.rot90(board, -2)  # ---> rotate the board by 90 degree of the matrix in opposite direction
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_right(board):
    # This function manipulate the the board to move right by the "Right key",
    # the function create new latest board that
    # was pushed right by player choice (or the Bot choice) like in real 2048 game.
    # The function returns the latest board (matrix) that moved right, if the move is made, and the score.
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, second_pushed_made = push_board_right(board)
    move_made = has_pushed or has_merged
    return board, move_made, score


"""def fixed_move(board):
    move_order = [move_left, move_up, move_down, move_right]
    for func in move_order:
        new_board, move_made, _ = func(board)                   ------> Test of confirming valid moves 
        if move_made:
            return new_board, True
    return board, False """


def random_move(board):
    # This function choosing a random move that is valid to make!
    # this function, return the latest board which in it a random move is made .
    # if no random moves are exist, meaning those moves are not valid, the function will
    # return the current board without any changes.
    move_made = False
    move_order = [move_right, move_up, move_down, move_left]
    while not move_made and len(move_order) > 0:
        move_index = np.random.randint(0, len(move_order))
        move = move_order[move_index]
        board, move_made, score = move(board)
        if move_made:
            return board, True, score
        move_order.pop(move_index)
    return board, False, score


def add_new_tile(board):
    # Add a new 2 or 4 title randomly to an empty cell
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
    tile_row_options, tile_col_options = np.nonzero(
        np.logical_not(board))
    tile_loc = np.random.randint(0, len(tile_row_options))
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return board

    # row = random.randint(0, 3)
    # col = random.randint(0, 3)
    # while board[row][col] != 0:
    # row = random.randint(0, 3)
    # col = random.randint(0, 3)
    # board[row][col] = random.choice([2, 4])
    # return board


def horizontal_move_exists(matrix):
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]:
                return True
    return False


def vertical_move_exists(matrix):
    for i in range(3):
        for j in range(4):
            if matrix[i][j] == matrix[i + 1][j]:
                return True
    return False


def check_for_win(board):
    return 2048 in board
