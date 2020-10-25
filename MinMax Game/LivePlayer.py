import operator

class LivePlayer:
    def __init__(self):
        self.loc = None

    def set_game_params(self, map):
        for i, row in enumerate(map):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
        # print('live player location set', self.loc)

    def set_rival_move(self, _):
        pass

    def tup_add(self, t1, t2):
        return tuple(map(operator.add, t1, t2))

    def make_move(self):
        assert self.loc is not None
        while True:
            d = input()
            # print('in make_move, current loc:', self.loc)
            if d == 'a':
                # print('going left')
                return 0, -1
            elif d == 'w':
                # print('going up')
                return 1, 0
            elif d == 'd':
                # print('going right')
                return 0, 1
            elif d == 's':
                # print('going down')
                return -1, 0

    def update_loc(self, loc):
        self.loc = loc

