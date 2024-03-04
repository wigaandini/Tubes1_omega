import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class GanasLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.current_position: Position

    def distance_to_self(self, object : Position):
        return (abs(self.current_position.x - object.x) + abs(self.current_position.y - object.y))

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        self.current_direction = board_bot.position
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            bots_position = [(d.position,d.id) for d in board.game_objects if d.type == "BotGameObject" and d.id != board_bot.id]
            print(bots_position)
            # sorted_bots_position = sorted(bots_position, key=lambda x: x[1])
            self.goal_position = bots_position[0][0]
            # Just roam around
            self.goal_position = None
        delta_x, delta_y = get_direction(
            self.current_position.x,
            self.current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
