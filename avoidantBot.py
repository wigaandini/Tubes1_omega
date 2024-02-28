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

def avoidantBot(board_bot: GameObject, board: Board) :
    diamonds = [diamond for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
    positionBot = board_bot.position
    blue_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamonds if B.properties.points == 1]
    red_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y), B.position) for B in diamonds if B.properties.points == 2]

    sorted_blue_diamond_distance = sorted(blue_diamond_distance, key=lambda x: x[0])
    sorted_red_diamond_distance = sorted(red_diamond_distance, key=lambda x: x[0])

    bots_on_board = board.bots
    for bot in bots_on_board:
        bot_position = bot.position
        print(f"Bot {bot.properties.name} is at position ({bot_position.x}, {bot_position.y})")
        distance_x = abs(bot_position.x - positionBot.x)
        distance_y = abs(bot_position.y - positionBot.y)

        if bot.properties.name != board_bot.properties.name and (distance_x == 0 and distance_y == 1) or (distance_x == 1 and distance_y == 0):
            if distance_x == 0:
                next_position = Position(y=-1, x=0) if bot_position.y < positionBot.y else Position(y=-1, x=0)
                return next_position
            elif distance_y == 0:
                next_position = Position(y=0, x=-1) if bot_position.x < positionBot.x else Position(y=0, x=1)
                return next_position

    if len(red_diamond_distance) == 0 :
        next_position = sorted_blue_diamond_distance[0][1]
    elif len(blue_diamond_distance) == 0 :
        next_position = sorted_red_diamond_distance[0][1]
    else :
        print("red ",sorted_red_diamond_distance[0][0])
        print("blue ",sorted_blue_diamond_distance[0][0])
        print("size ",board_bot.properties.diamonds)
        if len(blue_diamond_distance) == 1:
            x = 0
        else :
            x = 1
        if sorted_red_diamond_distance[0][0] < sorted_blue_diamond_distance[x][0] and board_bot.properties.diamonds <= 3:
            next_position = sorted_red_diamond_distance[0][1]
        else:
            next_position = sorted_blue_diamond_distance[0][1]
            print(next_position)
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
            self.goal_position = avoidantBot(board_bot, board)
        current_position = board_bot.position

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y