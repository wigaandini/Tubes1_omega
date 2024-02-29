import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class PrototypeLogicN(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.sorted_blue_diamond_distance: list[tuple[int, int, Position]] = []
        self.sorted_red_diamond_distance: list[tuple[int, int, Position]] = []
        self.sorted_red_diamond_distance_from_base: list[tuple[int, int, Position]] = []
        self.sorted_blue_diamond_distance_from_base: list[tuple[int, int, Position]] = []

    def nearest_Diamond(self, red_diamond_distance: list[tuple[int, Position]],
                        blue_diamond_distance: list[tuple[int, Position]],
                        currentLoad: int):
        if len(red_diamond_distance) == 0:
            self.goal_position = self.sorted_blue_diamond_distance[0][2]
        elif len(blue_diamond_distance) == 0:
            self.goal_position = self.sorted_red_diamond_distance[0][2]
        else:
            if len(blue_diamond_distance) == 1:
                x = 0
            else:
                x = 1
            if self.sorted_red_diamond_distance[0][0] < self.sorted_blue_diamond_distance[x][0] and currentLoad <= 3:
                self.goal_position = self.sorted_red_diamond_distance[0][2]
            else:
                self.goal_position = self.sorted_blue_diamond_distance[x][2]

    def nearest_Bot(self, nearby_bots: list[GameObject], current_position: Position):
        if nearby_bots:
            nearest_bot = min(nearby_bots, key=lambda bot: abs(bot.position.x - current_position.x) + abs(bot.position.y - current_position.y))
            self.goal_position = nearest_bot.position

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        base = board_bot.properties.base
        diamonds = [diamond for diamond in board.game_objects if diamond.type == 'DiamondGameObject']
        positionBot = board_bot.position
        blue_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y),
                                abs(B.position.x - base.x) + abs(B.position.y - base.y), B.position)
                                for B in diamonds if B.properties.points == 1]
        red_diamond_distance = [(abs(B.position.x - positionBot.x) + abs(B.position.y - positionBot.y),
                                abs(B.position.x - base.x) + abs(B.position.y - base.y), B.position)
                                for B in diamonds if B.properties.points == 2]

        self.sorted_blue_diamond_distance = sorted(blue_diamond_distance, key=lambda x: x[0])
        self.sorted_red_diamond_distance = sorted(red_diamond_distance, key=lambda x: x[0])
        self.sorted_blue_diamond_distance_from_base = sorted(blue_diamond_distance, key=lambda x: x[1])
        self.sorted_red_diamond_distance_from_base = sorted(red_diamond_distance, key=lambda x: x[1])

        if props.diamonds >= 3:
            self.nearest_Bot(board.game_objects, board_bot.position)
        else:
            nearby_bots_with_diamonds = [bot for bot in board.game_objects if bot.type == 'BotGameObject' and bot.id != board_bot.id and bot.properties.diamonds > 0]
            if nearby_bots_with_diamonds:
                self.nearest_Bot(nearby_bots_with_diamonds, board_bot.position)
            else:
                self.nearest_Diamond(red_diamond_distance, blue_diamond_distance, props.diamonds)

        current_position = board_bot.position

        # Check for nearby bots
        nearby_bots = [bot for bot in board.game_objects if bot.type == 'BotGameObject' and bot.id != board_bot.id]
        for bot in nearby_bots:
            if abs(bot.position.x - current_position.x) + abs(bot.position.y - current_position.y) == 1:
                # Attack nearby bot
                if bot.properties.diamonds > 0:
                    # Steal diamonds from the bot
                    bot.properties.diamonds -= 1
                    props.diamonds += 1
                    # Update goal position if the bot has fewer than 3 diamonds and there are nearby bots with diamonds
                    if props.diamonds < 3 and any(nbot.properties.diamonds > 0 for nbot in nearby_bots):
                        self.nearest_Bot([nbot for nbot in nearby_bots if nbot.properties.diamonds > 0], board_bot.position)
                        # Calculate direction towards the new goal position
                        delta_x, delta_y = get_direction(
                            current_position.x,
                            current_position.y,
                            self.goal_position.x,
                            self.goal_position.y,
                        )
                        return delta_x, delta_y

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
