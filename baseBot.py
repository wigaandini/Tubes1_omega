import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class BaseLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.sorted_blue_diamond_distance: list[tuple[int, Position]]
        self.sorted_red_diamond_distance: list[tuple[int, Position]]

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
                self.goal_position = self.sorted_red_diamond_distance[0][1]
            else:
                self.goal_position = self.sorted_blue_diamond_distance[0][1]
    

    def getBaseDistance(self, board_bot: GameObject, board: Board) :
        positionBot = board_bot.position
        base = board_bot.properties.base
        base_distance = abs(base.x - positionBot.x) + abs(base.y - positionBot.y)
        return base_distance


    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            bot_base_distance = self.getBaseDistance(board_bot, board)
            diamonds = [diamond for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
            positionBot = board_bot.position
            blue_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamonds if B.properties.points == 1]
            red_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamonds if B.properties.points == 2]

            self.sorted_blue_diamond_distance = sorted(blue_diamond_distance, key=lambda x: x[0])
            self.sorted_red_diamond_distance = sorted(red_diamond_distance, key=lambda x: x[0])
            # self.nearest_Diamond(red_diamond_distance,blue_diamond_distance, props.diamonds)
            if bot_base_distance != 0:
                if bot_base_distance < self.sorted_blue_diamond_distance[0][0] and bot_base_distance < self.sorted_red_diamond_distance[0][0] and props.diamonds != 0:
                    self.goal_position = board_bot.properties.base
                else:
                    self.nearest_Diamond(red_diamond_distance,blue_diamond_distance, props.diamonds)
            else:
                self.nearest_Diamond(red_diamond_distance,blue_diamond_distance, props.diamonds)

        current_position = board_bot.position

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
