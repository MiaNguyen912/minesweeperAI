# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
# 				agent in this file. You will write the 'getAction' function,
# 				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
# 				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        ########################################################################
        # 							YOUR CODE BEGINS						   #
        ########################################################################

        # NOTE: the first tile is uncovered automatically for user
        # NOTE: X and Y coordinates of World start at 1, not 0
        # NOTE: startX and starY are coordinates starting from 0

        self.__rowDimension = rowDimension
        self.__colDimension = colDimension
        self.__totalMines = totalMines
        self.__startX = startX   # the inital tile at (__startX, __startY) is guaranteed to be safe (0 mines around)
        self.__startY = startY
        self.__flagRemaining = totalMines
        self.__tilesCovered = ( rowDimension * colDimension - 1 )  # number of covered tiles (including flagged tiles)
        self.__tilesRemaining = ( rowDimension * colDimension - 1 )  # number of covered tiles (not including flagged tiles)
        self.__frontier = set() # set of tuples (use set to disallow duplication)
        self.__tilesToUncover = set()
        self.__previouslyUncoveredTile = (startX, startY)

        # create Effective label array:
        # - covered tiles: -1
        # - uncovered tiles: number of mines around them - number of flags around them
        # - flagged tiles: - 99

        # EXAMPLE:
        # __effectiveLabelArray = [
        # 							[-1, -1, -1, 0, -99],
        # 							[-1, -1, -1, -1, -1],
        # 							[-1, -1, -1, -1, -1],
        # 							[-1, -1, -1, -1, -1],
        # 							[-1, -1, -1, -1, -1],
        # 						  ]
        self.__effectiveLabelArray = [[-1 for _ in range(colDimension)] for _ in range(rowDimension)]
        self.__effectiveLabelArray[startX][startY] = 0
        print(self.__effectiveLabelArray)

    def getAction(self, number: int) -> "Action Object":
        print("percept number: ", number)
        if number == 0:
            self.__frontier.add(self.__previouslyUncoveredTile)

        ########################################################################
        # 							YOUR CODE BEGINS						   #
        ########################################################################

        # action = AI.Action.LEAVE
        # action = AI.Action.UNFLAG
        # action = AI.Action.FLAG
        # action = AI.Action.UNCOVER

        # if done solving the world, leave
        if self.__tilesCovered == self.__totalMines:
            return Action(AI.Action.LEAVE)
        
        if len(self.__frontier) == 0:
            return Action(AI.Action.LEAVE)

        # if there are tiles waiting to be uncovered, uncover them
        print("frontier: ", self.__frontier)
        print("tiles to uncover: ", self.__tilesToUncover)
        if len(self.__tilesToUncover) > 0:
            print("pop __tilesToUncover")
            x, y = self.__tilesToUncover.pop()
            self.__previouslyUncoveredTile = (x,y)
            return Action(AI.Action.UNCOVER, x, y)

        # scan the frontier
        if len(self.__frontier) > 0:
            print("pop __frontier")
            processedTile = self.__frontier.pop()
            processedTile_X, processedTile_Y = processedTile

            
            for i in range(processedTile_X - 1, min(processedTile_X + 1 + 1, self.__rowDimension)):
                for j in range(processedTile_Y - 1, min(processedTile_Y + 1 + 1, self.__colDimension)):
                    if self.__effectiveLabelArray[i][j] == -1:
                        self.__tilesToUncover.add((i, j))
            print("tiles to uncover: ", self.__tilesToUncover)

                            
        nextTile_x, nextTile_y = self.__tilesToUncover.pop()
        self.__previouslyUncoveredTile = (nextTile_x, nextTile_y)
        return Action(AI.Action.UNCOVER, nextTile_x, nextTile_y)

