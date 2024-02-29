import random
import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class PortalLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.portal: tuple[Position, Position]
        self.sorted_red_diamond_distance: list[tuple[int,int, Position]]
        self.sorted_blue_diamond_distance: list[tuple[int,int, Position]]
    
    def getDistance(self, A: Position, B: Position) :
        return (abs(B.x - A.x) + abs(B.y - A.y))
    
    def getPortal(self, board_bot: GameObject, board : Board) :
        portal_position = [d.position for d in board.game_objects if d.type == 'TeleportGameObject']
        bot_position = board_bot.position
        if (self.getDistance(portal_position[0], bot_position) < self.getDistance(portal_position[1], bot_position)):
            nearest_portal = portal_position[0]
            second_portal = portal_position[1]
        else :
            nearest_portal = portal_position[1]
            second_portal = portal_position[0]
        return nearest_portal, second_portal
    
    def logicPortal(self, result : bool, leng : int, diamonds_position : list[Position], board_bot: GameObject, final_distance : Optional[Position]) :
        distance_from_bot = self.getDistance(diamonds_position[leng - 1], board_bot.position)
        distance_with_portal = self.getDistance(self.portal[0], board_bot.position) + self.getDistance(self.portal[1], diamonds_position[leng - 1])
        if distance_with_portal <= distance_from_bot :
            temp_final_distance = distance_with_portal
            result = True
        else :
            temp_final_distance = distance_from_bot
            result = False
        if temp_final_distance < final_distance :
            if result:
                goal_position = self.portal[0]
            else :
                goal_position = diamonds_position[leng - 1]
        diamonds_position.pop()
        leng -= 1
        return goal_position, final_distance
    
    def greedydiamondportal(self, blue_diamonds_position : list[Position], red_diamonds_position : list[Position], board_bot: GameObject) :
        result_blue = False
        result_red = False
        goal_blue : Optional[tuple[Position, int]] = None
        goal_red : Optional[tuple[Position, int]] = None
        leng_blue = len(blue_diamonds_position)
        leng_red = len(red_diamonds_position)
        pass_leng_blue = leng_blue
        pass_leng_red = leng_red
        final_distance_blue = blue_diamonds_position[pass_leng_blue - 1]
        final_distance_red = blue_diamonds_position[pass_leng_red - 1]
        if (leng_blue == 0) :
            goal_blue = self.logicPortal(result_blue, pass_leng_blue, blue_diamonds_position, board_bot, final_distance_blue)
        if (leng_blue == 0) :
            goal_red =  self.logicPortal(result_red, pass_leng_red, blue_diamonds_position, board_bot, final_distance_red)
        while pass_leng_blue != 0 and pass_leng_red != 0:
            if (pass_leng_blue != 0) :
                goal_blue = self.logicPortal(result_blue, pass_leng_blue, blue_diamonds_position, board_bot, final_distance_blue)
            if (pass_leng_red != 0) :
                goal_red = self.logicPortal(result_red, pass_leng_red, blue_diamonds_position, board_bot, final_distance_red)
        if (goal_blue != None and goal_red != None) :
            if goal_red[1] <= goal_blue[1] :
                self.goal_position = goal_red[0]
            else:
                self.goal_position = goal_blue[0]
        elif goal_blue == 0 :
            self.goal_position = goal_blue[0]
        else :
            self.goal_position = goal_red[0]

    # def nearest_Diamond(self, diamond_distance : list[tuple[Position]], currentLoad : int) :
    #     while len(diamond_distance):
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            self.portal = self.getPortal(board_bot, board)
            blue_diamonds = [diamond.position for diamond in board.game_objects if diamond.type == 'DiamondGameObject' if diamond.properties.points == 1]
            red_diamonds = [diamond.position for diamond in board.game_objects if diamond.type == 'DiamondGameObject' if diamond.properties.points == 2]
            
            if (board_bot.position in self.portal) :
                self.nearest_Diamond(red_diamonds, blue_diamonds, props.diamonds)
            else :
                self.greedydiamondportal(blue_diamonds, red_diamonds, board_bot)
            

        current_position = board_bot.position

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y

            # if True:
            #     if board_bot.position.x > board_bot.properties.base.x :
            #         xMin = board_bot.properties.base.x
            #         xMax = board_bot.position
            #     else :
            #         xMax = board_bot.properties.base.x
            #         xMin = board_bot.position
            #     if board_bot.position.y > board_bot.properties.base.y :
            #         yMin = board_bot.properties.base.y
            #         yMax = board_bot.position
            #     else :
            #         yMax = board_bot.properties.base.y
            #         yMin = board_bot.position