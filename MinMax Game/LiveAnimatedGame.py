#!/#!/usr/bin/env python3

from Game import Game
from LiveAnimation import LiveAnimation
from LivePlayer import LivePlayer
from MapsGenerator import *
from SimplePlayer import SimplePlayer
import time
import sys, os
# from PyQt4.QtCore import pyqtRemoveInputHook

class LiveAnimatedGame:
    def __init__(self, size, block_locations, starts, player_1, player_2, moves='regular', time_to_make_a_move=2):
        assert hasattr(player_1, 'set_game_params')
        assert hasattr(player_2, 'set_game_params')
        assert hasattr(player_1, 'make_move')
        assert hasattr(player_2, 'make_move')
        assert hasattr(player_1, 'set_rival_move')
        assert hasattr(player_2, 'set_rival_move')
        self.time_to_make_a_move = time_to_make_a_move
        self.game = Game(size, block_locations, starts, moves)
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1.set_game_params(self.game.board.get_map_for_player_i(1))
        self.player_2.set_game_params(self.game.board.get_map_for_player_i(2))
        self.players = [self.player_1, self.player_2]
        self.live_animation = LiveAnimation(self.game.board.get_map_for_player_i(1), starts, self.player_1, self.player_2,
                                            animation_func=self.animate_func)
        self.live_animation.start_game()

    def player_cant_move(self, player_index):
        board = self.game.board
        player_loc = self.game.board.get_player_location(player_index + 1)
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        all_next_locations = [self.game.tup_add(player_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if self.game.board.loc_is_in_board(loc)]
        possible_next_locations = [loc for loc in in_board_next_locations if board[loc] == 0]
        return len(possible_next_locations) == 0

    def animation_0_1(self):
       return self.live_animation.get_starting_state()


    def animate_func(self, t):
        if t < 2:
          return self.animation_0_1()

        player_index = t % 2
        # print('TURN', t, 'player', player_index + 1)
        if self.player_cant_move(player_index):
            if self.player_cant_move(1 - player_index):
                print('####################')
                print('####################')
                print("     It's a Tie!")
                print('####################')
                print('####################')
                sys.stdout = open(os.devnull, 'w')
                input('Press Enter To Close Animation')
                exit()
            else:
                players_colors = [None, 'Blue', 'Red']
                print('####################')
                print('####################')
                print(" ", players_colors[(1 - player_index) + 1], "Player Won!")
                print('####################')
                print('####################')
                sys.stdout = open(os.devnull, 'w')
                input('Press Enter To Close Animation')
                exit()

        if isinstance(self.players[player_index], LivePlayer):
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
                input('Press Enter To Close Animation')
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
        return self.live_animation.do_animation_func_staff_with_pos(loc)

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
    d = {'time_to_make_a_move': 2, 'map': 0, 'time_to_set_game_param': 2}
    flags_input = sys.argv[3:]
    assert len(flags_input) % 2 == 0, 'bad flags'
    while len(flags_input) > 0:
        flag = flags_input[0]
        assert flag[0] == '-'
        flag = flag[1:]
        val = flags_input[1]
        if flag == 'move_time':
            d['time_to_make_a_move'] = float(val)
        elif flag == 'set_params_time':
            d['time_to_set_game_param'] = float(val)
        else:
            assert flag == 'board', 'unknown flag ' + flag
            d['map'] = int(val)
        flags_input = flags_input[2:]
    return d


if __name__ == '__main__':
    # print('runing')
    player_1_type = sys.argv[1]
    player_2_type = sys.argv[2]
    module_1 = __import__(player_1_type)
    module_2 = __import__(player_2_type)
    player_1 = get_player(player_1_type, module_1)
    player_2 = get_player(player_2_type, module_2)

    d = create_flags()
    map_index = d['map']
    map = maps[map_index]
    time_to_make_a_move = d['time_to_make_a_move']

    print('Starting Game')
    print(player_1_type, 'VS', player_2_type)
    print('Board', map_index)
    print('Players (besides LivePlayer) have', time_to_make_a_move, 'seconds to make a move')
    LiveAnimatedGame(map[0], map[1], map[2], player_1=player_1, player_2=player_2,
                     time_to_make_a_move=time_to_make_a_move)