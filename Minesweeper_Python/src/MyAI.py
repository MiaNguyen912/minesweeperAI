# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action

MINE = 100
COVERED_UNKNOWN = 200
COVERED_SAFE = 300
labeled = [MINE, COVERED_UNKNOWN, COVERED_SAFE]

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		# Constructor Initializations
		self._rowDimension = rowDimension
		self._colDimension = colDimension
		self._totalMines = totalMines # keep track of how many mines are left in the game
		self.startingMines = totalMines # Constant: the number of mines we started with
		self._startX = startX
		self._startY = startY

		# Game Initialization
		self.board = [[COVERED_UNKNOWN] * self._colDimension for _ in range(self._rowDimension)] 
		self.prevMove = (startX, startY)
		self.prevAction = AI.Action.UNCOVER
		self.remainingTiles = (rowDimension * colDimension -1) # num of covered tiles (flagged and not flagged); the first tile is opened automatically, so deduct 1
		self.numCoveredUnflaggedTiles = (rowDimension * colDimension -1) # num of covered tiles that are not flagged
		self.numFlaggedTiles = 0
  
		self.frontier_uncovered = set()   # list of frontier tiles that are uncovered
		self.frontier_covered = set()   # list of tiles to be uncovered
		self.mines = set() # list of mines to be flagged
		

	def inRange(self, i, j):
		return (i >= 0 and i < self._rowDimension) and (j >= 0 and j < self._colDimension)


	def get_frontier_uncovered(self):
		# Check each tile on the board, if it is uncovered and has at least 1 covered tile around -> it should be in the frontier_uncovered
		frontier_uncovered = set()
		for row in range(self._rowDimension):
			for col in range(self._colDimension):
				if self.board[row][col] <= 8: # 8 is the max number of mine around a tile, the effective lable <= 8 means the tile is uncovered and is not mine/flagged
					numMine, adjacentCovered = self.getNumAdjacentMinesAndCovered(row,col)
					if len(adjacentCovered) > 0:
						frontier_uncovered.add((row,col))
		return frontier_uncovered


	def get_frontier_covered(self):
     	# Check each tile on the board, if it is covered and has at least 1 uncovered tile around -> it should be in the frontier_covered
		frontier_covered = set()
		for row in range(self._rowDimension):
			for col in range(self._colDimension):
				if self.board[row][col] == COVERED_UNKNOWN or self.board[row][col] == COVERED_SAFE:					
					unCoveredTiles = set()
					for i in range(row - 1, row + 2):
						for j in range(col - 1, col + 2):
							if self.inRange(i, j) and self.board[i][j] <= 8:
								unCoveredTiles.add((i, j))
					if len(unCoveredTiles) > 0:
						frontier_covered.add((row,col))
		return frontier_covered


	def getNumAdjacentMinesAndCovered(self, x, y):
		numMines = 0
		coveredTiles = set()
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and (i, j) != (x, y):
					if (self.board[i][j] == MINE):
						numMines += 1
					elif(self.board[i][j] == COVERED_UNKNOWN or self.board[i][j] == COVERED_SAFE):
						coveredTiles.add((i, j))
		return numMines, coveredTiles


	def flagTile(self, x, y):
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and i != x and j != y and self.board[x][y] not in labeled:
					self.board[i][j] -= 1
					if self.board[i][j] == 0:
						_, coveredTiles = self.getNumAdjacentMinesAndCovered(i, j)
						for coveredTile in coveredTiles:
							coveredX, coveredY = coveredTile
							if self.board[coveredX][coveredY] != COVERED_SAFE:
								self.board[coveredX][coveredY] = COVERED_SAFE
								self.frontier_covered.append(coveredTile)
		




	def updateBoardNewMove(self, number):
		x, y = self.prevMove

		# numAdjacentMines is the number of known mines so far, covered tiles are all adjacent covered tiles that are not bombs
		numAdjacentMines, coveredTiles = self.getNumAdjacentMinesAndCovered(x, y)

		# compute effective label by taking its hint number and subtracing all known mines around it
		self.board[x][y] = number - numAdjacentMines

		# if the effective label is equal to the number of covered tiles then all uncovered tiles are mines
		if number == len(coveredTiles):
			for i, j in coveredTiles:
				self.board[i][j] = MINE
				self._totalMines -= 1	
				self.mines.add((i,j))

		# if the hint number is equal to the number of mines we are aware of or if it's 0, then the rest must be safe
		if number == 0 or number == numAdjacentMines:
			for i, j in coveredTiles:
				if self.board[i][j] != COVERED_SAFE:
					self.board[i][j] = COVERED_SAFE
					self.frontier_covered.add((i, j))




	def print_status(self):
		print("\n")
		for row in self.board:
			print(row)
		print("Frontier_uncovered: ", self.frontier_uncovered)
		print("frontier_covered: ", self.frontier_covered)
		print("mines: ", self.mines)
		print("Num covered tiles: ", self.remainingTiles)
		print("Num covered, unflagged tiles: ", self.numCoveredUnflaggedTiles)
		print("Num flagged tiles: ", self.numFlaggedTiles)
		print("\n")

		
	def getAction(self, number: int) -> "Action Object":
		self.updateBoardNewMove(number)

		# If the game is over -> uncover all remaining tiles and leave (no more tiles left to uncover)
		if (self.numFlaggedTiles == self.startingMines):
			for x in range(self._rowDimension):
				for y in range(self._colDimension):
					if self.board[x][y] == COVERED_UNKNOWN:
						self.frontier_covered.add((x,y))


		if self.numCoveredUnflaggedTiles == 0:
			self.print_status()
			print("No more covered unflagged tile, Leaving game")
			return Action(AI.Action.LEAVE)
		
		
		
		# self.frontier_uncovered = self.get_frontier_uncovered()
		# self.frontier_covered = self.get_frontier_covered()
		self.print_status()

		if self.frontier_covered:
			moveX, moveY = self.frontier_covered.pop()
			self.prevMove = (moveX, moveY)
			self.prevAction = AI.Action.UNCOVER
			self.remainingTiles -= 1
			self.numCoveredUnflaggedTiles -=1
			return Action(AI.Action.UNCOVER, moveX, moveY)

		
		elif self.mines: 
			# if frontier is empty, it means no safe tile left -> start flagging known mines
			flagX, flagY = self.mines.pop()
			self.prevMove = (flagX, flagY)
			self.prevAction = AI.Action.FLAG
			self.numCoveredUnflaggedTiles -=1
			self.numFlaggedTiles += 1
			return Action(AI.Action.FLAG, flagX, flagY)
		
		else:
			# start checking for unknown mines		
			for x in range(self._rowDimension):
				for y in range(self._colDimension):
					numAdjacentMines, coveredTiles = self.getNumAdjacentMinesAndCovered(x, y)

					# if effective number == number of covered tiles, all covered tiles are mines
					if self.board[x][y] == len(coveredTiles) and len(self.mines) + self.numFlaggedTiles < self._totalMines:
						for i in range(max(0, x - 1), min(x + 1 + 1, self._rowDimension)):
							for j in range(max(0, y - 1), min(y + 1 + 1, self._colDimension)):
								if self.board[i][j] == COVERED_UNKNOWN:
									self.board[i][j] = MINE
									self.mines.add((i,j))
				
			# if no mine was detected, use probability to detect mines
			# if (len(self.mines) == 0):
				



		prev_X, prev_Y = self.prevMove
		print("Do nothing in this loop")
		return Action(self.prevAction, prev_X, prev_Y) # means do nothing




					
		
		


		
				






		




		
        

