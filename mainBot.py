import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class PrototypeLogic(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.sorted_blue_diamond_distance: list[tuple[int,int, Position]]
        self.sorted_red_diamond_distance: list[tuple[int,int, Position]]
        self.sorted_red_diamond_distance_from_base: list[tuple[int,int, Position]]
        self.sorted_blue_diamond_distance_from_base: list[tuple[int,int, Position]]

    def nearest_Diamond(self, red_diamond_distance : list[tuple[int,Position]], 
                   blue_diamond_distance : list[tuple[int,Position]], 
                   currentLoad : int) :
        if len(red_diamond_distance) == 0 :
            self.goal_position = self.sorted_blue_diamond_distance[0][1]
        elif len(blue_diamond_distance) == 0 :
            self.goal_position = self.sorted_red_diamond_distance[0][1]
        else :
            if len(blue_diamond_distance) == 1:
                x = 0
            else :
                x = 1
            if self.sorted_red_diamond_distance[0][0] < self.sorted_blue_diamond_distance[x][0] and currentLoad <= 3:
                self.goal_position = self.sorted_red_diamond_distance[0][2]
            else:
                self.goal_position = self.sorted_blue_diamond_distance[0][2]
    
    def time_to_base(self, board_bot: GameObject) :
        props = board_bot.properties
        score_needed = 5 - props.diamonds
        if len(self.sorted_red_diamond_distance_from_base[score_needed - 1][1]) < score_needed :
            score_needed = 1
        elif len(self.sorted_blue_diamond_distance_from_base[score_needed - 1][1]) == score_needed :
            score_needed = 1
        best_red_diamond_distance = self.sorted_red_diamond_distance_from_base[score_needed - 1][1]
        best_blue_diamond_distance = self.sorted_blue_diamond_distance_from_base[score_needed - 1][1]
        best_red_diamond = self.sorted_red_diamond_distance_from_base[score_needed - 1][2]
        best_blue_diamond = self.sorted_blue_diamond_distance_from_base[score_needed - 1][2]
        if best_red_diamond_distance < best_blue_diamond_distance and props.diamonds <= 3:
            self.goal_position = best_red_diamond
        else:
            self.goal_position = best_blue_diamond

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        base = board_bot.properties.base
        diamonds = [diamond for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
        positionBot = board_bot.position
        blue_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), abs(B.position.x - base.x) + abs(B.position.y - base.y), B.position) for B in diamonds if B.properties.points == 1]
        red_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), abs(B.position.x - base.x) + abs(B.position.y - base.y), B.position) for B in diamonds if B.properties.points == 2]

        self.sorted_blue_diamond_distance = sorted(blue_diamond_distance, key=lambda x: x[0])
        self.sorted_red_diamond_distance = sorted(red_diamond_distance, key=lambda x: x[0])
        self.sorted_blue_diamond_distance_from_base = sorted(blue_diamond_distance, key=lambda x: x[1])
        self.sorted_red_diamond_distance_from_base = sorted(red_diamond_distance, key=lambda x: x[1])
        
        if props.diamonds >= 3 :
            self.time_to_base(board_bot)
        else :
            self.nearest_Diamond(red_diamond_distance, blue_diamond_distance, props.diamonds)

        current_position = board_bot.position

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
