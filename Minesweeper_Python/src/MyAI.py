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
        self.__numFlagRemaining = totalMines
        self.__numTilesCovered = ( rowDimension * colDimension)  # number of covered tiles (including flagged tiles)
        self.__numTilesRemaining = ( rowDimension * colDimension)  # number of covered tiles (not including flagged tiles)
        self.__frontier_covered = set() # list of tiles to be uncovered
        self.__frontier_uncovered = set() # list of uncovered tiles, waiting for their surrounding tiles to be added to the frontier
        self.__currentTile = (startX, startY)
        self.__effectiveLabelArray = [[-1 for _ in range(colDimension)] for _ in range(rowDimension)]

        # Effective label array:
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





    def getAction(self, number: int) -> "Action Object":
        ########################################################################
        # 							YOUR CODE BEGINS						   #
        ########################################################################
        
		# update __frontier_uncovered:
        self.__frontier_uncovered.add(self.__currentTile)
        
        # update __numTilesCovered, __numTilesRemaining
        self.__numTilesCovered -= 1
        self.__numTilesRemaining -= 1
        
		# update __effectiveLabelArray:
        current_x, current_y = self.__currentTile
        numFlagsAround = 0
        for i in range(current_x - 1, min(current_x + 1 + 1, self.__rowDimension)):
                for j in range(current_y - 1, min(current_y + 1 + 1, self.__colDimension)):
                    if self.__effectiveLabelArray[i][j] == -99:
                       numFlagsAround += 1
        self.__effectiveLabelArray[current_x][current_y] = number - numFlagsAround
        
		
		
        
		 # if done solving the world, leave
        if self.__numTilesCovered == self.__totalMines:
            return Action(AI.Action.LEAVE)

        
		# if current tile has no bombs around, add all covered tiles around it into __frontier_covered
        if number == 0:
            for i in range(current_x - 1, min(current_x + 1 + 1, self.__rowDimension)):
                for j in range(current_y - 1, min(current_y + 1 + 1, self.__colDimension)):
                    if self.__effectiveLabelArray[i][j] == -1:     # -1 means the tile has not been uncovered
                        self.__frontier_covered.add((i, j))
                        
						
        # print status
        print("\n\n")
        for row in self.__effectiveLabelArray:
            print(row)
        print("__frontier_uncovered: ", self.__frontier_uncovered)
        print("__frontier_covered: ", self.__frontier_covered)
        

        # if there are tiles waiting to be uncovered, uncover them
       
        if len(self.__frontier_covered) > 0:
            # print("pop __tilesToUncover")
            next_x, next_y = self.__frontier_covered.pop()
            self.__currentTile = (next_x, next_y)
            return Action(AI.Action.UNCOVER, next_x, next_y)

        # scan the __frontier_uncovered
        if len(self.__frontier_uncovered) > 0:
            # print("pop __frontier")
            current_x, current_y = self.__frontier_uncovered.pop()

            
            for i in range(current_x - 1, min(current_x + 1 + 1, self.__rowDimension)):
                for j in range(current_y - 1, min(current_y + 1 + 1, self.__colDimension)):
                    if self.__effectiveLabelArray[i][j] == -1:
                        self.__frontier_covered.add((i, j))
                        

                            
        nextTile_x, nextTile_y = self.__frontier_covered.pop()
        self.__currentTile = (nextTile_x, nextTile_y)
        return Action(AI.Action.UNCOVER, nextTile_x, nextTile_y)

