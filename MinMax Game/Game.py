from Board import Board
from MapsGenerator import *

class Game:
    def __init__(self, size, block_locations, starts, moves='regular'):
        self.size = size
        self.board = Board(size, block_locations, starts)
        self.moves = moves
        self.current_player = 1
        self.player_1 = None
        self.player_2 = None
        self.paths = [None, [starts[0]], [starts[1]]]

    def set_players(self, player_1, player_2):
        '''
        :params: the players implements functions "set_game_params", "make_move" and "set_rival_move".
        set_game_params - receive the map and the players locations.
        make move -  returns the next cell to which the player moves.
        set_rival_move - get the cell to which the rival moved to.
        '''
        assert hasattr(player_1, 'set_game_params')
        assert hasattr(player_1, 'set_game_params')
        assert hasattr(player_1, 'make_move')
        assert hasattr(player_2, 'make_move')
        assert hasattr(player_1, 'set_rival_move')
        assert hasattr(player_2, 'set_rival_move')

        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1.set_game_params(self.board.get_map_for_player_i(1))
        move = player_1.make_move(5)
        loc = self.tup_add(move, self.board.get_player_location(1))
        self.check_move(loc)
        self.paths[1].append(loc)
        self.player_2.set_game_params(self.board.get_map_for_player_i(2))
        # we are now all set to run the game!

    def switch_players(board):
        if board.current_player == 1:
            board.current_player = 2
        else:
            board.current_player = 1

    def check_move(self, cell_loc, switch_players=True):
        # we also switch players in here...
        if self.moves == 'regular':
            if not (0 <= cell_loc[0] < self.size[0] and 0 <= cell_loc[1] < self.size[1]):
                # print('here 1')
                return False
            if not self.board[cell_loc] == 0:
                # print('here 2 ==>', self.board[cell_loc])
                return False
            prev_player_location = self.board.get_player_location()
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            if not any(self.tup_add(prev_player_location, move) == cell_loc for move in directions):
                # print('moved from', prev_player_location, 'to', cell_loc)
                return False

        self.board.update_loc(cell_loc)
        if switch_players:
            self.switch_players()
        return True

    def tup_add(self, t1, t2):
        return tuple(map(operator.add, t1, t2))

    def check_victory(self, player_index):
        if player_index == 1:
            first = 2
            second = 1
        else:
            first = 1
            second = 2
        if self.moves == 'regular':
            # we are checkin if the current player is stack, if so, the other player wins.
            player_loc = self.board.get_player_location(first)
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            all_next_locations = [self.tup_add(player_loc, direction) for direction in directions]
            in_board_next_locations = [loc for loc in all_next_locations if self.board.loc_is_in_board(loc)]
            possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
            if len(possible_next_locations) == 0:
                return first
            player_loc = self.board.get_player_location(second)
            all_next_locations = [self.tup_add(player_loc, direction) for direction in directions]
            in_board_next_locations = [loc for loc in all_next_locations if self.board.loc_is_in_board(loc)]
            possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
            if len(possible_next_locations) == 0:
                return second
        return 0

    def run_game(self):
        # starting with player 2 because player 1 moved at the "set_players"
        players = [None, self.player_1, self.player_2]  # pushing None so players[i] = player_i
        while self.check_victory() == 0:
            # print('player', self.current_player, 'is making a move...')
            move = players[self.current_player].make_move(5)
            new_loc = self.tup_add(move, self.board.get_player_location(self.board.current_player))
            self.paths[self.current_player].append(new_loc)
            assert self.check_move(new_loc)
            players[self.current_player].set_rival_move(new_loc)

        print('####################')
        print('####################')
        print("    Player", self.check_victory(), "Won!")
        print('####################')
        print('####################')
        return self.paths[1:]

