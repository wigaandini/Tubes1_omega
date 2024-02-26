import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def nearestDiamond(board_bot: GameObject, board: Board) :
    diamond_positions = [diamond for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
    positionBot = board_bot.position
    blue_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamond_positions if B.properties.points == 1]
    red_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamond_positions if B.properties.points == 2]

    sorted_blue_diamond_distance = sorted(blue_diamond_distance, key=lambda x: x[0])
    sorted_red_diamond_distance = sorted(red_diamond_distance, key=lambda x: x[0])

    if sorted_red_diamond_distance[0] < sorted_blue_diamond_distance[1]:
        next_position = sorted_red_diamond_distance[0][1]
    else:
        next_position = sorted_blue_diamond_distance[0][1]
    return next_position

class PrototypeLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            # self.goal_position = None
            self.goal_position = nearestDiamond(board_bot, board)
        current_position = board_bot.position

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
