import numpy as np


class Board:
    def __init__(self, size, block_locations, starts):
        '''
        :param size: of shape (m, n)
        :param initial_block_locations: list of map entries
        :param starts: list of map entries, of size 2

        The map is represented with a numpy array:
            -1 - blocked.
             0 - free.
             1 - player 1.
             2 - player 2.

        The bard assumes player 1 starts, and turns are switched every time.
        '''
        self.size = size
        self.map = np.zeros(size)
        for i, j in block_locations:
            self.map[i][j] = -1

        for player_index, (i, j) in enumerate(starts):
            self.map[i][j] = player_index + 1

        self.players_locations = starts
        self.current_player = 1

    def __getitem__(self, indexes):
        '''
        :param item: indexes. Usage: self[i, j]
        :return: True <=> this cell is free.
        '''
        i = indexes[0]
        j = indexes[1]
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1], 'out of self'
        item = self.map[i][j]
        return item

    def __setitem__(self, indexes, value):
        # For inner use.
        '''
        :param item: indexes. Usage: board[i, j]
        :return: True <=> this cell is free.
        '''
        i = indexes[0]
        j = indexes[1]
        self.map[i][j] = value

    def update_loc(self, loc):
        assert self[loc] == 0, 'location ' + str(loc) + ' is not free: ' + str(self[loc])
        prev_loc = self.players_locations[self.current_player - 1]
        self[loc] = self.current_player
        self.players_locations[self.current_player - 1] = loc
        self[prev_loc] = -1
        self.switch_players()

    def switch_players(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def get_map_for_player_i(self, i):
        map_copy = self.map.copy()
        player_i_loc = self.players_locations[i - 1]
        if i == 1:
            other_player_loc = self.players_locations[1]
        else:
            other_player_loc = self.players_locations[0]
        map_copy[player_i_loc] = 1
        map_copy[other_player_loc] = 2
        return map_copy

    def get_player_location(self, player_index=None):
        if player_index is None:
            return self.players_locations[self.current_player - 1]
        else:
            return self.players_locations[player_index - 1]

    def loc_is_in_board(self, loc):
        i = loc[0]
        j = loc[1]
        return 0 <= i < self.size[0] and 0 <= j < self.size[1]
