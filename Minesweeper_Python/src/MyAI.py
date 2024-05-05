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
        self.__frontier = set([(startX, startY)]) # set of tuples (use set to disallow duplication)
        self.__tilesToUncover = set()

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
        pass

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

        # if there are tiles waiting to be uncovered, uncover them
        print("frontier: ", self.__frontier)
        print("tiles to uncover: ", self.__tilesToUncover)
        if len(self.__tilesToUncover) > 0:
            x, y = self.__tilesToUncover.pop()
            return Action(AI.Action.UNCOVER, x, y)

        # scan the frontier
        if len(self.__frontier) > 0:
            processedTile = self.__frontier.pop()
            processedTile_X, processedTile_Y = processedTile
            x_inArray, y_inArray = processedTile_X, processedTile_Y

            if self.__effectiveLabelArray[x_inArray][y_inArray] == 0:
                for i in range(x_inArray - 1, min(x_inArray + 1 + 1, self.__rowDimension)):
                    for j in range(y_inArray - 1, min(y_inArray + 1 + 1, self.__colDimension)):
                        if self.__effectiveLabelArray[i][j] == -1:
                            self.__tilesToUncover.add((i, j))
                            
        nextTile_x, nextTile_y = self.__tilesToUncover.pop()
        return Action(AI.Action.UNCOVER, nextTile_x, nextTile_y)

