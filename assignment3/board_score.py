"""
board_score.py
Implements functions to:
- compute the final score on a Go board
- determine the winner.
"""

import numpy as np
from board_util import where1d, BORDER, BLACK, WHITE, GoBoardUtil

def score_board(board):
    """ Score board from Black's point of view """
    score = 0
    counted = np.full(board.maxpoint, False, dtype=bool)
    for point in range(board.maxpoint):
            color = board.get_color(point)
            if color == BORDER or (point in counted):
                continue
            if color == BLACK:
                score += 1
            elif color == WHITE:
                score -= 1
            else:
                black_flag = False
                white_flag = False
                empty_points = where1d(board.connected_component(point))
                for p in empty_points:
                    counted[p] = True 
                    # TODO faster to boolean-or the whole array
                    if board.find_neighbor_of_color(p, BLACK):
                        black_flag = True
                    if board.find_neighbor_of_color(p, WHITE):
                        white_flag = True
                    if black_flag and white_flag:
                        break
                if black_flag and not white_flag:
                    score += len(empty_points)
                if white_flag and not black_flag:
                    score -= len(empty_points)
    return score

def winner(board):
    current_player = board.current_player
    legal_moves = GoBoardUtil.generate_legal_moves(board, current_player)
    if legal_moves == None:
        opp = GoBoardUtil.opponent(current_player)
        return opp
    else:
        return None
    # score = score_board(board)
    # if score > 0:
    #     return BLACK
    # elif score < 0:
    #     return WHITE
    # else:
    #     return None
