import numpy as np

from game_functions import random_move, \
    move_down, move_left, \
    move_right, move_up, \
    add_new_tile

"""Now we will create the AI method to try and beat the game 2048!
   I will be using an approach called monte carlo tree search.
   let's think of the game as decision tree, the root node is the starting position of the game.
   and the leaf nodes are the ending positions classified as win or losses.
   we want to find a path from the root node starting position to a winning leaf node and do it
   as fast as possible.
   I will mention that is a difficult task, it takes hundreds of moves to win the game and we are
   dealing with imperfect information because new values will be added to the board at random
   each turn to determine our move we will evaluate a random selection of paths of our decision tree.
   This is where the "Monte carlo tree search" comes in.
   Monte carlo is a class of methods that model an event by generating a great number of simulations of 
   that event and then randomly sampling outcomes from these simulations.
   this method approach will be creating an AI that plays 2048 is to generate a great number of games that end when either:
   *A. game ends with win or loss  
   *B. some move limit is reached  
   Now' we will call each of these games outcomes a path, we then score each of these paths based on the sum of the values
   of all the tiles that were merged during the gameplay. The paths are then grouped by their first move and the best move with
   the best average score of its paths is selected.
   Note: its promise 80% of winning or close to be at winning state 
     """


def ai_move(board, searches_per_move, search_length):
    first_moves = [move_left, move_up, move_down,
                   move_right]  # splitting our search paths by first move (for each move)
    first_move_scores = np.zeros(4)  # list for its respective score
    for first_move_index in range(4):
        # playing the first move
        # We will loop over an index for each possible move and then try and play that move.
        # Playing that function will return in the following order and the board after
        # the move was played whether or not the was actually playable and the score from that move.
        first_move_function = first_moves[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        if first_move_made:
            # if the move was played then we will add a new tile in an empty square and add the score
            # to the total scores we are tracking
            board_with_first_move = add_new_tile(board_with_first_move)
            first_move_scores[first_move_index] += first_move_score
        else:
            # if the move wasn't played then we will continue on to the next first move
            continue
        for later_moves in range(searches_per_move):
            # rest of the moves to played in the search tree
            # from the position after the first move has been played
            # we are making a number of searches per move.
            # we set the move set the move number to 1
            # since only the first move has been played
            move_number = 1
            search_board = np.copy(board_with_first_move)  # copy the board after the first move
            game_valid = True  # set a boolean variable for make sure the game is valid
            while game_valid and move_number < search_length:
                # defining a while loop which keeps looping while the game
                # is still valid, and the move number is less than the search length
                # at each move a random move out of available moves is made.
                # The random move function has three returned values:
                # 1) The board with the move played
                # 2) Whether or not position given to the function is valid
                # 3) The score for the move
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    # if the game is valid, then the new tiles will be added
                    search_board = add_new_tile(search_board)
                    # the score from that move will be added to the
                    # first move scores counter
                    first_move_scores[first_move_index] += score
                    move_number += 1  # the move number will be incremented by 1
                    """then this just repeats until either the game becomes invalid meaning there are
                    not more playable moves OR we have reached the search length"""
    # Last step is outside of all the loops which just defines the index of the move with the best score
    best_move_index = np.argmax(first_move_scores)
    best_move = first_moves[best_move_index]
    # then that move and its validity is returned
    search_board, game_valid, score = best_move(board)
    return search_board, game_valid, score
    # if all the moves are invalid then game valid will be false and the given position wasn't
    # valid in the first place
