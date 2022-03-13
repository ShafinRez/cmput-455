#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import EMPTY, GoBoardUtil, BLACK, WHITE
from board import GoBoard


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
        self.policy = 'random'

    def randomSimulation(self, state, move, player):
        tempState = state.copy()
        while True:
            currentPlayer = tempState.current_player
            randomMove = state.generate_random_move(state, player)
            if move == None:
                return BLACK + WHITE - currentPlayer
            tempState.play_move(move, currentPlayer)
    

    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=False)

    def simulate(self, state, move, toplay):
        if self.policy == 'random':
            return self.randomSimulation(state, move, toplay)

    def undoMove(self, state, move):
        state.board[move] = EMPTY
        currentPlayer = state.current_player
        state.current_player = WHITE + BLACK - currentPlayer


    def Randomgenmove(self, state):
        assert not state.endOfGame()
        moves = state.get_empty_points()
        #randomize moves
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            legal = state.is_legal(move, state.current_player)
            if legal:
                move = moves[i]
                score[i] = self.simulate(state, move)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        assert best in state.legalMoves()
        return best


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()