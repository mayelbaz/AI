from OrderedAlphaBetaPlayer import *


class ContestPlayer(OrderedAlphaBetaPlayer):
    def __init__(self):
        super().__init__()
        self.loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.white_slots_list = []
        self.enemy_loc = None
        self.initial_white_slots = None



    def Alpha_Beta_MinMax_Aux(self, board, depth: int, leafs, our_loc, enemy_loc, turn, alpha, beta):

        game_state = self.check_state(self.board, self.loc, enemy_loc)

        # stop condition
        if game_state != CONTINUE:
            leafs[0] += 1
            return game_state
        if depth == 0:
            h_value = self.total_state_score(board, our_loc)
            return h_value

        # Player turn
        if turn == OUR_TURN:
            best_score = -np.inf
            board[our_loc] = -1
            children = []
            for d in self.directions:
                i = our_loc[0] + d[0]
                j = our_loc[1] + d[1]
                if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                    new_loc = (i, j)
                    children.append(new_loc)
            board[our_loc] = 1
            children.sort(key=lambda child: self.total_state_score(board, child), reverse=True)
            for new_loc in children:
                board[our_loc] = -1
                board[new_loc] = 1
                score = self.Alpha_Beta_MinMax_Aux(board, depth - 1, leafs, new_loc, enemy_loc, ENEMY_TURN,
                                                   alpha,
                                                   beta)
                if score > best_score:
                    best_score = score
                board[new_loc] = 0
                board[our_loc] = 1
                alpha = max(best_score, alpha)
                if best_score >= beta:
                    return np.inf
            return best_score

        # enemy turn
        else:

            worst_score = np.inf
            board[enemy_loc] = -1
            children = []
            for d in self.directions:
                i = enemy_loc[0] + d[0]
                j = enemy_loc[1] + d[1]
                if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                    new_loc = (i, j)
                    children.append(new_loc)
            board[enemy_loc] = 2
            children.sort(key=lambda child: self.total_state_score(board, child))
            for new_loc in children:
                board[new_loc] = 2
                board[enemy_loc] = -1
                score = self.Alpha_Beta_MinMax_Aux(board, depth - 1, leafs, our_loc, new_loc, OUR_TURN, alpha,
                                                   beta)
                if score < worst_score:
                    worst_score = score
                board[new_loc] = 0
                beta = min(worst_score, beta)
                board[enemy_loc] = 2
                if worst_score <= alpha:
                    return -np.inf
            return worst_score
