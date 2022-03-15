#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, BLACK, WHITE, PASS
from board import GoBoard
from simulation_util import writeMoves, select_best_move
from ucb import runUcb
from board_score import winner
from pattern_util import PatternUtil
from sys import stdin, stdout, stderr
from board_util import coord_to_point


class Go0:
    def __init__(self):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go0"
        self.version = 1.0
        self.num_sim = 10
        self.limit = 10
        self.selection = "rr"
        self.policy = "random"

    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.num_sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return None
        moves.append(None)
        if self.selection == "ucb":
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = runUcb(self, cboard, C, moves, color)
            return best
        else:
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            # writeMoves(cboard, moves, moveWins, self.num_sim)
            return select_best_move(board, moves, moveWins)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        nuPasses = 0
        for _ in range(self.limit):
            color = board.current_player
            if self.policy == "random":
                move = GoBoardUtil.generate_random_move(board, color, False)
            else:
                move = PatternUtil.generate_move_with_filter(
                    board, self.use_pattern, False
                )

            board.play_move(move, color)
            if move == PASS:
                nuPasses += 1
            else:
                nuPasses = 0
            if nuPasses >= 2:
                break
        return winner(board)

    # def randomSimulation(self, state, move, player):
    #     tempState = state.copy()
    #     tempState.play_move(move, player)
    #     while True:
    #         currentPlayer = tempState.current_player
    #         randomMove = GoBoardUtil.generate_random_move(state, player, False)
    #         if randomMove == None:
    #             return BLACK + WHITE - currentPlayer
    #         tempState.play_move(move, currentPlayer)

    def getLegalMoves(self, state, colour):
        emptyPos = state.get_empty_points()
        moves = []
        for pos in emptyPos:
            if state.is_legal(pos, colour):
                moves.append(pos)
        return moves 

    # def simulate(self, state, move, toplay):
    #     if self.policy == 'random':
    #         return self.randomSimulation(state, move, toplay)

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
