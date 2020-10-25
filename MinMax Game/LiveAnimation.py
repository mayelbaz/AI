#!/#!/usr/bin/env python3
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class LiveAnimation:
    def __init__(self, map, starting_locations, player_1, player_2, animation_func):
        self.animation_func = animation_func
        assert len(starting_locations) == 2, 'Currently supporting 2 players only'
        self.map = map
        self.starting_locations = starting_locations
        self.players = [player_1, player_2]
        aspect = len(self.map[0]) / len(self.map)

        # Colors:
        self.board_colors = {'free': 'gray', 'stepped on': 'gray'}
        self.players_colors = ['blue', 'red']

        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)

        # create boundary patch
        x_min = -0.5
        y_min = -0.5
        x_max = len(self.map[0]) - 0.5
        y_max = len(self.map) - 0.5
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        # patches = board_patch + map_patches + agent_patches
        self.board_patch = [Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, facecolor='none', edgecolor='gray')]
        self.map_patches = []
        for i in range(len(self.map)):
            self.map_patches.append([])
            for j in range(len(self.map[0])):
                if self.map[i][j] != 0:
                    face_color = self.board_colors['stepped on']
                    self.map_patches[i].append(
                        Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=face_color, edgecolor='black', fill=True))
                else:
                    face_color = self.board_colors['free']
                    self.map_patches[i].append(
                        Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=face_color, edgecolor='black', fill=False))

        # painting the starting locations of the agents:
        self.map_patches[self.starting_locations[0][0]][self.starting_locations[0][1]].fill = True
        self.map_patches[self.starting_locations[1][0]][self.starting_locations[1][1]].fill = True


        # create agents:
        self.T = 0
        self.agents = []
        self.agent_patches = []
        for i in range(len(self.starting_locations)):
            self.agents.append(Circle(tuple(reversed(self.starting_locations[i])), 0.3, facecolor=self.players_colors[i], edgecolor='black'))
            self.agents[i].original_face_color = self.players_colors[i]
            self.agent_patches.append(self.agents[i])
            self.T = max(self.T, len(self.starting_locations[i]) - 1)
        
        global animation
        animation = FuncAnimation(self.fig, self.animation_func,
                                                 init_func=self.init_func,
                                                 frames=int(self.T + 1) * 10,
                                                 interval=600,  # change game speed here
                                                 blit=False)
        self.turn = 0

    def save(self, file_name, speed):
        self.animation.save(
            file_name,
            fps=10 * speed,
            dpi=200,
            savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    def start_game(self):
        # print('starting game')
        plt.show()

    @staticmethod
    def show():
        plt.show()

    def init_func(self):
        for p in self.board_patch + sum(self.map_patches, []) + self.agent_patches:
            self.ax.add_patch(p)
        return self.board_patch + sum(self.map_patches, []) + self.agents

    def do_animation_func_staff_with_pos(self, pos):
        pos = tuple(reversed(pos))
        self.agents[self.turn].center = pos

        i = pos[1]
        j = pos[0]
        self.map_patches[i][j].fill = True

        self.turn = 1 - self.turn
        return self.board_patch + sum(self.map_patches, []) + self.agents

    def get_starting_state(self):
        return self.board_patch + sum(self.map_patches, []) + self.agents

    @staticmethod
    def get_state(t, path):
        if int(t) <= 0:
            return np.array(path[0])
        elif int(t) >= len(path):
            return np.array(path[-1])
        else:
            pos_last = np.array(path[int(t) - 1])
            pos_next = np.array(path[int(t)])
            pos = (pos_next - pos_last) * (t - int(t)) + pos_last
            return pos