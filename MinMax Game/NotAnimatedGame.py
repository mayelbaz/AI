#!/#!/usr/bin/env python3

from Game import Game
from LivePlayer import LivePlayer
from MapsGenerator import *


from SimplePlayer import SimplePlayer
import time
import sys, os
# from PyQt4.QtCore import pyqtRemoveInputHook

class NotAnimatedGame:
    def __init__(self, size, block_locations, starts, player_1, player_2, moves='regular', time_to_make_a_move=2,
                 print_game_in_terminal=True):
        assert hasattr(player_1, 'set_game_params')
        assert hasattr(player_2, 'set_game_params')
        assert hasattr(player_1, 'make_move')
        assert hasattr(player_2, 'make_move')
        assert hasattr(player_1, 'set_rival_move')
        assert hasattr(player_2, 'set_rival_move')
        self.print_game_in_terminal = print_game_in_terminal
        self.time_to_make_a_move = time_to_make_a_move
        self.game = Game(size, block_locations, starts, moves)
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1.set_game_params(self.game.board.get_map_for_player_i(1))
        self.player_2.set_game_params(self.game.board.get_map_for_player_i(2))
        self.players = [self.player_1, self.player_2]
        self.t = 0
        self.run_game()

    def player_cant_move(self, player_index):
        board = self.game.board
        player_loc = self.game.board.get_player_location(player_index + 1)
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        all_next_locations = [self.game.tup_add(player_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if self.game.board.loc_is_in_board(loc)]
        possible_next_locations = [loc for loc in in_board_next_locations if board[loc] == 0]
        return len(possible_next_locations) == 0

    def run_game(self):
        while True:
            if self.t == 0 and self.print_game_in_terminal:
                print('\nInitial board:')
                board = self.game.board.get_map_for_player_i(1)
                self.print_board_to_terminal(board)
            player_index = self.t % 2
            # print('TURN', t, 'player', player_index + 1)
            if self.player_cant_move(player_index):
                if self.player_cant_move(1 - player_index):
                    print('####################')
                    print('####################')
                    print("     It's a Tie!")
                    print('####################')
                    print('####################')
                    sys.stdout = open(os.devnull, 'w')
                    exit()
                else:
                    print('####################')
                    print('####################')
                    print("    Player", (1 - player_index) + 1, "Won!")
                    print('####################')
                    print('####################')
                    sys.stdout = open(os.devnull, 'w')
                    exit()

            if isinstance(self.players[player_index], LivePlayer):
                print('Player', player_index + 1, 'insert your move.')
                sys.stdout = open(os.devnull, 'w')
                move = self.players[player_index].make_move()
                sys.stdout = sys.__stdout__
            else:
                start = time.time()
                move = self.players[player_index].make_move(self.time_to_make_a_move)
                end = time.time()
                diff = end - start
                if diff > self.time_to_make_a_move:
                    print()
                    print('####################')
                    print('####################')
                    print(" Time Up For Player", player_index + 1)
                    print("    Player", 1 - player_index + 1, "Won!")
                    print('####################')
                    print('####################')
                    exit()
            prev_loc = self.game.board.get_player_location(player_index + 1)
            # print('player is at loc', prev_loc)
            loc = (prev_loc[0] + move[0], prev_loc[1] + move[1])
            if isinstance(self.players[player_index], LivePlayer):
                # print('this is a live player turn')
                while not self.game.check_move(loc, switch_players=False):
                    # print('illegal move to location', loc)
                    sys.stdout = open(os.devnull, 'w')
                    move = self.players[player_index].make_move()
                    sys.stdout = sys.__stdout__
                    loc = (prev_loc[0] + move[0], prev_loc[1] + move[1])
                self.players[player_index].update_loc(loc)
                self.players[1 - player_index].set_rival_move(loc)
                self.game.switch_players()
            else:
                # print('Agent', player_index + 1, 'moved to', loc)
                assert self.game.check_move(loc), 'illegal move'
                self.players[1 - player_index].set_rival_move(loc)

            if self.print_game_in_terminal:
                board = self.game.board.get_map_for_player_i(1)
                print('\nBoard after player', player_index + 1, 'made a move')
                self.print_board_to_terminal(board)
            self.t += 1

    def print_board_to_terminal(self, board):
        board_to_print = np.flipud(board.copy())
        # print(board_to_print)
        print('_' * len(board_to_print[0]) * 4)
        for row in board_to_print:
            row = [str(int(x)) if x != -1 else 'X' for x in row]
            print(' | '.join(row))
            print('_' * len(row) * 4)


def get_player(player_type, module):
    if player_type == 'LivePlayer':
        player = LivePlayer()
    elif player_type == 'SimplePlayer':
        player = SimplePlayer()
    elif player_type == 'MinimaxPlayer':
        player = module.MinimaxPlayer()
    elif player_type == 'AlphaBetaPlayer':
        player = module.AlphaBetaPlayer()
    elif player_type == 'OrderedAlphaBetaPlayer':
        player = module.OrderedAlphaBetaPlayer()
    elif player_type == 'HeavyAlphaBetaPlayer':
        player = module.HeavyAlphaBetaPlayer()
    elif player_type == 'LiteAlphaBetaPlayer':
        player = module.LiteAlphaBetaPlayer()
    elif player_type == 'ContestPlayer':
        player = module.ContestPlayer()
    else:
        print('bad input')
        exit(-1)
    return player

def create_flags():
    d = {'time_to_make_a_move': 2, 'map': 0, 'time_to_set_game_param': 2, 'print_in_terminal': True}
    flags_input = sys.argv[3:]
    # assert len(flags_input) % 2 == 0, 'bad flags'
    while len(flags_input) > 0:
        flag = flags_input[0]
        assert flag[0] == '-'
        flag = flag[1:]
        if flag != 'dont_print_game':
            val = flags_input[1]
        else:
            val = None

        if flag == 'move_time':
            d['time_to_make_a_move'] = float(val)
        elif flag == 'dont_print_game':
            d['print_in_terminal'] = False
            flags_input = flags_input[1:]
            continue
        elif flag == 'set_params_time':
            d['time_to_set_game_param'] = float(val)
        else:
            assert flag == 'board', 'unknown flag ' + flag
            d['map'] = int(val)
        flags_input = flags_input[2:]
    return d


if __name__ == '__main__':
    # print('runing')
    args = sys.argv.copy()

    player_1_type = args[1]
    player_2_type = args[2]
    module_1 = __import__(player_1_type)
    module_2 = __import__(player_2_type)
    player_1 = get_player(player_1_type, module_1)
    player_2 = get_player(player_2_type, module_2)

    d = create_flags()
    map_index = d['map']
    map = maps[map_index]
    time_to_make_a_move = d['time_to_make_a_move']
    print_in_terminal = d['print_in_terminal']

    print('Starting Game')
    print(player_1_type, 'VS', player_2_type)
    print('Board', map_index)
    print('Players (besides LivePlayer) have', time_to_make_a_move, 'seconds to make a move')
    NotAnimatedGame(map[0], map[1], map[2], player_1=player_1, player_2=player_2,
                     time_to_make_a_move=time_to_make_a_move, print_game_in_terminal=print_in_terminal)