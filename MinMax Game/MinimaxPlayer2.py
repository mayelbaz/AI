import operator
from typing import *
import time as t
import numpy as np
from scipy.spatial import distance as dist
from _collections import defaultdict


PLAYER_WON = 100
PLAYER_LOST = -100
GAME_TIED = -10
CONTINUE = 'NOT_A_LEAF'

NO_MOVES = -1

OUR_TURN = 1
ENEMY_TURN = 2

class MinimaxPlayer2:
    def __init__(self):
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

    def player_loc_in_sim(self, board):
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    return tuple(i, j)

    def check_state(self, board, loc, enemy_loc):
        # enemy_x, enemy_y = self.find_enemy(board)
        # enemy_loc = (enemy_x, enemy_y)
        num_of_enemy_moves = len(self.find_adjacent(loc=enemy_loc, board=board))
        buffer_steps = self.state_score_reachable_slots(board=board, loc=loc)
        num_of_player_moves = len(self.find_adjacent(loc=loc, board=board))
        # enemy has no further move & player has no further moves
        if num_of_enemy_moves == 0 and num_of_player_moves == 0:
            return GAME_TIED
        if num_of_enemy_moves != 0 and num_of_player_moves == 0:
            return PLAYER_LOST
        if num_of_player_moves != 0 and num_of_enemy_moves == 0 and buffer_steps >= 3:
            # print(f"in location:{loc} -\n buffer is:{buffer_steps}\n")
            return PLAYER_WON
        return CONTINUE


    # Our heuristic, takes into account:
    # 1) num of available steps - like Simple Player.
    # 2) distance to enemy.
    # 3) num of reachable slots.

    def total_state_score(self, board, loc):
        score_simple_player = self.state_score_simple_player(board=board, loc=loc)
        score_get_close_to_enemy = self.state_score_get_close_to_enemy(board=board, loc=loc)
        score_reachable_slots = self.state_score_reachable_slots(board=board, loc=loc)
        score_tuple = (score_simple_player / 4, -score_get_close_to_enemy / (len(board) + len(board[0])),
                       score_reachable_slots / self.initial_white_slots)
        score = 0.2 * score_tuple[0] + 0.4 * score_tuple[1] + 0.4* score_tuple[2]
        # print(f"\nin location:{loc} -\n score_simple_player:{score_simple_player}\n "
        #     f"score_get_close_to_enemy:{score_get_close_to_enemy}\n "
        #     f"score_reachable_slots:{score_reachable_slots}\n "
        #     f"normalized score:{score}\n ")
        return score

    def state_score_simple_player(self, board, loc):
        num_steps_available = 0
        # e_x, e_y = self.find_enemy(board)
        # adjacent_to_enemy = self.find_adjacent((e_x, e_y), board)
        # print(adjacent_to_enemy)
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                num_steps_available += 1

        if num_steps_available == 0:
            return NO_MOVES
        else:
            return 4 - num_steps_available

    '''
    :param self: self
    :param board: the current game board
    :param loc: Tuple (i,j) of player's location

    Calculates the number of reachable slots from the player's given location
    '''

    # def state_score_reachable_slots(self, board, loc):
    #     e_x, e_y = self.find_enemy(board)
    #     adjacent_to_enemy = self.find_adjacent((e_x, e_y), board)
    #     nodes_set = {(loc[0], loc[1])}  # start with a set containing only the root node
    #     tmp_set = {(loc[0], loc[1])}  # functions as Queue
    #     visited = {(loc[0], loc[1])}  # avoid repeats
    #     while len(tmp_set) > 0:
    #         slot = tmp_set.pop()
    #         visited.add(slot)
    #         neighbors = self.find_adjacent(slot, board)
    #         for neighbor in neighbors:
    #             if neighbor not in visited and neighbor not in adjacent_to_enemy:
    #                 tmp_set.add(neighbor)
    #                 nodes_set.add(neighbor)
    #     return len(nodes_set)-1

    def state_score_reachable_slots(self, board, loc):
        e_x, e_y = self.find_enemy(board)
        adjacent_to_enemy = self.find_adjacent((e_x, e_y), board)
        nodes_set = {(loc[0], loc[1])}  # start with a set containing only the root node
        tmp_set = {(loc[0], loc[1])}  # functions as Queue
        visited = {(loc[0], loc[1])}  # avoid repeats
        edges_list = []
        while len(tmp_set) > 0:
            slot = tmp_set.pop()
            visited.add(slot)
            neighbors = self.find_adjacent(slot, board)
            for neighbor in neighbors:
                if neighbor not in adjacent_to_enemy:
                    edges_list.append((slot, neighbor))
                if neighbor not in adjacent_to_enemy and neighbor not in visited:
                    tmp_set.add(neighbor)
                    nodes_set.add(neighbor)
        G = defaultdict(list)
        for (v, u) in edges_list:
            G[v].append(u)
            G[u].append(v)

        all_paths = self.DFS(G,loc, len(self.board)+len(self.board[0]))
        max_len = max(len(p) for p in all_paths)
        return max_len

    def find_adjacent(self, loc: Tuple[int, int], board):
        adjacent = []
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                adjacent.append((i, j))
        return adjacent

    def state_score_get_close_to_enemy(self, board, loc):
        e_x, e_y = self.find_enemy(board=board)
        enemy_location = (e_x, e_y)
        return dist.cityblock(loc, enemy_location)

    def find_enemy(self, board):
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 2:
                    return i, j
        # print("oh oh")

    def count_ones(self, board):
        counter = 0
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    counter += 1
        return counter

    def clac_time(self, num_leaves, last_iteration_time):
        num_v = (num_leaves - 2) / 2 + num_leaves
        time_per_v = last_iteration_time / num_v
        iteration_time = time_per_v * (num_v + 3 * num_leaves)
        return iteration_time


    def make_move(self, time):  # time parameter is not used, we assume we have enough time.

        last_iteration_time=0
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
        move, leafs = self.Minimax(board=self.board, depth=d, leafs=leafs_l,start_time= ID_start_time, time_lim=time, last_it_time=last_iteration_time)
        last_iteration_time = (t.time() - ID_start_time)
        # print("time: ", last_iteration_time)
        next_iteration_max_time = self.clac_time(leafs, last_iteration_time)
        time_until_now = t.time() - ID_start_time
        while time_until_now + next_iteration_max_time + 0.5 < time:
            d += 1
            iteration_start_time = t.time()
            move, leafs = self.Minimax(board=self.board, depth=d, leafs=leafs_l, start_time= ID_start_time, time_lim=time, last_it_time=last_iteration_time)
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

    def Minimax(self, board, depth, leafs, start_time,time_lim, last_it_time):
        # print("start MinMax")
        # best_move = self.directions[0]  # just to initialize
        best_move = None  # just to initialize
        our_loc = self.loc
        e_x, e_y = self.find_enemy(board)
        enemy_loc = (e_x, e_y)
        board[our_loc] = -1
        best_score = -np.inf
        leafs_count = leafs[0]
        for move in self.directions:
            i = our_loc[0] + move[0]
            j = our_loc[1] + move[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:
                # print(f"i is:{i}  j is:{j}\n")
                new_loc = (i, j)
                board[new_loc] = 1
                # self.print_board_to_terminal(board)
                leafs[0] = 0
                if t.time() - start_time + last_it_time >= time_lim:
                    break
                score = self.Minimax_aux(board, depth, leafs, new_loc, enemy_loc, OUR_TURN)
                # print("num leafs: ", leafs[0])
                # print("location score: ", score)
                # print("best score: ", best_score)
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
                    best_move= d
        # print("best move is:", best_move)
        # print(f"considering location:{our_loc}  best move is:{best_move}  with a score of {best_score}\n")
        return best_move, leafs_count

    def Minimax_aux(self, board, depth, leafs, our_loc, enemy_loc, turn):

        game_state = self.check_state(self.board, self.loc, enemy_loc)

        if game_state != CONTINUE:
            leafs[0] += 1
            return game_state

        if depth == 0:
            state_h_val = self.total_state_score(board, our_loc)
            return state_h_val

        # player turn
        if turn == OUR_TURN:
            best_score = -np.inf
            board[our_loc] = -1
            for d in self.directions:
                i = our_loc[0] + d[0]
                j = our_loc[1] + d[1]

                if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j] == 0:  # then move is legal
                    new_loc = (i, j)
                    board[new_loc] = 1
                    score = self.Minimax_aux(board, depth - 1, leafs, new_loc, enemy_loc, ENEMY_TURN)
                    if score > best_score:
                        best_score = score
                    board[new_loc] = 0

            board[our_loc] = 1
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
                    score = self.Minimax_aux(board, depth - 1, leafs, our_loc, new_loc, OUR_TURN)
                    if score < worst_score:
                        worst_score = score
                    board[new_loc] = 0


            board[enemy_loc] = 2
            return worst_score


    def set_rival_move(self, loc):
        self.board[self.enemy_loc] = -1
        self.board[loc] = 2
        self.enemy_loc = loc
        self.white_slots_list.remove(loc)

    def DFS(self, G, v, depth, seen=None, path=None):

        if seen is None: seen = []
        if path is None: path = [v]

        seen.append(v)

        paths = []
        if depth == 0:
            return paths
        seen.append(v)
        for t in G[v]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(self.DFS(G, t, depth-1, seen[:], t_path))
        return paths



