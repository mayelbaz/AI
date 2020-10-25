class SimplePlayer:
    def __init__(self):
        self.loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                    break

    def state_score(self, board, loc):
        num_steps_available = 0
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                num_steps_available += 1

        if num_steps_available == 0:
            return -1
        else:
            return 4 - num_steps_available

    def count_ones(self, board):
        counter = 0
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    counter += 1
        return counter

    def make_move(self, time):  # time parameter is not used, we assume we have enough time.

        assert self.count_ones(self.board) == 1

        prev_loc = self.loc
        self.board[prev_loc] = -1

        assert self.count_ones(self.board) == 0

        best_move, best_move_score, best_new_loc = None, float('-inf'), None
        for d in self.directions:
            i = self.loc[0] + d[0]
            j = self.loc[1] + d[1]

            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                new_loc = (i, j)
                # print('prev loc', prev_loc, 'new_loc:', new_loc, 'move:', (i, j))
                assert self.board[new_loc] == 0
                self.board[new_loc] = 1
                assert self.count_ones(self.board) == 1

                score = self.state_score(board=self.board, loc=(i, j))
                if score > best_move_score:
                    best_move, best_move_score, best_new_loc = d, score, new_loc
                self.board[new_loc] = 0
                assert self.count_ones(self.board) == 0


        if best_move is None:
            # print(self.board)
            exit()

        self.board[best_new_loc] = 1

        assert self.count_ones(self.board) == 1

        self.loc = best_new_loc
        # print('returning move', best_move)
        return best_move

    def set_rival_move(self, loc):
        self.board[loc] = -1
