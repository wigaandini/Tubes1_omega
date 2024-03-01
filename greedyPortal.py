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
    
    def logicPortal(self, diamonds_position : list[Position], board_bot: GameObject) :
        distance_from_bot = self.getDistance(diamonds_position[-1], board_bot.position)
        distance_with_portal = self.getDistance(self.portal[0], board_bot.position) + self.getDistance(self.portal[1], diamonds_position[-1])
        if distance_with_portal < distance_from_bot :
            result = True
            temp_final_distance = distance_with_portal
        else :
            result = False
            temp_final_distance = distance_from_bot
        return temp_final_distance, result
    
    def logicDiamond(self, diamonds_position : list[Position], board_bot: GameObject) :
        distance_from_bot = self.getDistance(diamonds_position[-1], board_bot.position)
        return distance_from_bot

    def greedyNearestDiamond(self, blue_diamonds_position : list[Position], red_diamonds_position : list[Position], board_bot: GameObject) :
        goal_blue : Optional[Position] = None
        goal_red : Optional[Position] = None
        leng_blue = len(blue_diamonds_position)
        leng_red = len(red_diamonds_position)
        if (leng_blue != 0) :
            final_distance_blue = self.getDistance(blue_diamonds_position[leng_blue - 1], board_bot.position)
        if (leng_red != 0) :
            final_distance_red = self.getDistance(red_diamonds_position[leng_red - 1], board_bot.position)
        while leng_blue != 0 or leng_red != 0:
            if (leng_blue != 0) :
                temp_blue = self.logicDiamond(blue_diamonds_position, board_bot)
                if temp_blue < final_distance_blue :
                    final_distance_blue = temp_blue
                    goal_blue = blue_diamonds_position[-1]
                blue_diamonds_position.pop()
                leng_blue -= 1
            if (leng_red != 0) :
                temp_red = self.logicDiamond(red_diamonds_position, board_bot)
                if temp_red < final_distance_red :
                    final_distance_red = temp_red
                    goal_red = red_diamonds_position[-1]
                red_diamonds_position.pop()
                leng_red -= 1
        if (goal_blue != None and goal_red != None) :
            if final_distance_red <= final_distance_blue and board_bot.properties.diamonds != 4 :
                self.goal_position = goal_red
            else:
                self.goal_position = goal_blue
        elif goal_blue == None :
            self.goal_position = goal_red
        else :
            self.goal_position = goal_blue
    
    def greedyDiamondPortal(self, blue_diamonds_position : list[Position], red_diamonds_position : list[Position], board_bot: GameObject) :
        goal_position_blue : Optional[Position] = None
        goal_position_red : Optional[Position] = None
        leng_blue = len(blue_diamonds_position)
        leng_red = len(red_diamonds_position)
        if (leng_blue != 0) :
            final_distance_blue = self.getDistance(blue_diamonds_position[-1], board_bot.position)
        if (leng_red != 0) :
            final_distance_red = self.getDistance(red_diamonds_position[-1], board_bot.position)
        while leng_blue != 0 or leng_red != 0:
            if (leng_blue != 0) :
                temp_position_blue = self.logicPortal(blue_diamonds_position, board_bot)
                temp_final_distance_blue = temp_position_blue[0]
                if temp_final_distance_blue < final_distance_blue :
                    final_distance_blue = temp_final_distance_blue
                    if temp_position_blue[1]:
                        goal_position_blue = self.portal[0]
                    else :
                        goal_position_blue = blue_diamonds_position[-1]
                blue_diamonds_position.pop()
                leng_blue -= 1
            if (leng_red != 0) :
                temp_position_red = self.logicPortal(red_diamonds_position, board_bot)
                temp_final_distance_red = temp_position_red[0]
                if temp_final_distance_red < final_distance_red :
                    final_distance_red = temp_final_distance_red
                    if temp_position_red[1]:
                        goal_position_red = self.portal[0]
                    else :
                        goal_position_red = red_diamonds_position[-1]
                red_diamonds_position.pop()
                leng_red -= 1
        if (goal_position_blue != None and goal_position_red != None) :
            if final_distance_red <= final_distance_blue and board_bot.properties.diamonds != 4:
                self.goal_position = goal_position_red
            else:
                self.goal_position = goal_position_blue
        elif goal_position_blue == None :
            self.goal_position = goal_position_red
        else :
            self.goal_position = goal_position_blue
    
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
                self.greedyNearestDiamond(blue_diamonds, red_diamonds, board_bot)
            else :
                self.greedyDiamondPortal(blue_diamonds, red_diamonds, board_bot)
                print(self.portal, self.goal_position)
            

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