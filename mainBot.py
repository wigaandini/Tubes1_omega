import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def nearestDiamond(board_bot: GameObject, board: Board) :
    diamond_positions = [diamond.position for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
    positionBot = board_bot.position
    diamond_distance = [(abs(B.x - positionBot.x) + abs(B.y - positionBot.y), B) for B in diamond_positions]

    sorted_diamond_distance = sorted(diamond_distance, key=lambda x: x[0])

    return sorted_diamond_distance[0][1]

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
