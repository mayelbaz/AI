from MinimaxPlayer import *


class OrderedAlphaBetaPlayer(MinimaxPlayer):
    def __init__(self):
        super().__init__()
        self.loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.white_slots_list = []
        self.enemy_loc = None
        self.initial_white_slots = None

    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                if val == 0:
                    self.white_slots_list.append((i, j))
                if val == 2:
                    self.enemy_loc = (i, j)
        self.initial_white_slots = len(self.white_slots_list)

    def make_move(self, time):
        last_iteration_time = 0
        # assert self.count_ones(self.board) == 1
        ID_start_time = t.time()
        # print("\n\n\nstart iteration\n\n\n")
        if len(self.find_adjacent(self.loc, board=self.board)) == 1:
            # print("only one neighbore\n")
            for d in self.directions:
                i = self.loc[0] + d[0]
                j = self.loc[1] + d[1]
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:
                    self.board[self.loc] = -1
                    self.loc = (i, j)
                    self.board[i][j] = 1
                    return d

        leafs_l = [0]
        d = 1
        move, leafs = self.Alpha_Beta(board=self.board, depth=d, leafs=leafs_l, start_time=ID_start_time,
                                      time_lim=time,
                                      last_it_time=last_iteration_time)
        last_iteration_time = (t.time() - ID_start_time)
        # print("time: ", last_iteration_time)
        next_iteration_max_time = self.clac_time(leafs, last_iteration_time)
        time_until_now = t.time() - ID_start_time
        while time_until_now + next_iteration_max_time + 0.5 < time:
            d += 1
            iteration_start_time = t.time()
            move, leafs = self.Alpha_Beta(board=self.board, depth=d, leafs=leafs_l, start_time=ID_start_time,
                                          time_lim=time, last_it_time=last_iteration_time)
            last_iteration_time = (t.time() - iteration_start_time)
            next_iteration_max_time = self.clac_time(leafs, last_iteration_time)
            time_until_now = t.time() - ID_start_time
        new_loc_x = self.loc[0] + move[0]
        new_loc_y = self.loc[1] + move[1]
        self.board[self.loc] = -1
        self.loc = (new_loc_x, new_loc_y)
        self.board[new_loc_x][new_loc_y] = 1
        # print(" total time: ", time_until_now)
        # print(f"for location:{self.loc}  chosen move is:{move}\n*******************")
        return move

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
                    board[new_loc] = 1
                    score = self.Alpha_Beta_MinMax_Aux(board, depth - 1, leafs, new_loc, enemy_loc, ENEMY_TURN,
                                                       alpha,
                                                       beta)
                    if score > best_score:
                        best_score = score
                    board[new_loc] = 0
                alpha = max(best_score, alpha)
                board[our_loc] = 1
                if best_score >= beta:
                    return np.inf
            return best_score

        # enemy turn
        else:

            worst_score = np.inf
            board[enemy_loc] = -1
            for d in self.directions:
                i = enemy_loc[0] + d[0]
                j = enemy_loc[1] + d[1]
                if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                    new_loc = (i, j)
                    board[new_loc] = 2
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

    def Alpha_Beta(self, board, depth, leafs, start_time, time_lim, last_it_time):

        alpha = -np.inf
        beta = np.inf
        best_move = None  # just to initialize
        our_loc = self.loc
        e_x, e_y = self.find_enemy(board)
        enemy_loc = (e_x, e_y)
        board[our_loc] = -1
        best_score = -np.inf
        leafs_count = leafs[0]
        children = []
        for move in self.directions:
            i = our_loc[0] + move[0]
            j = our_loc[1] + move[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:
                new_loc = (i, j)
                children.append(new_loc)

        children.sort(key=lambda child: self.total_state_score(board, child), reverse=True)
        for new_loc in children:
            board[new_loc] = 1
            leafs[0] = 0
            if t.time() - start_time + last_it_time >= time_lim:
                break
            score = self.Alpha_Beta_MinMax_Aux(board, depth, leafs, new_loc, enemy_loc, OUR_TURN, alpha, beta)
            i = new_loc[0] - our_loc[0]
            j = new_loc[1] - our_loc[1]
            move = (i, j)
            if score > best_score:
                best_score = score
                best_move = move
                leafs_count = leafs[0]
            board[new_loc] = 0

        board[our_loc] = 1
        if best_move == None:
            for d in self.directions:
                i = self.loc[0] + d[0]
                j = self.loc[1] + d[1]
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:
                    best_move = d

        return best_move, leafs_count
