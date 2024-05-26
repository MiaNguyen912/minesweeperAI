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
COVERED = 200
SAFE = 0
labeled = [MINE, COVERED, SAFE]

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
		self.board = [[COVERED] * self._colDimension for _ in range(self._rowDimension)] 
		self.currentMove = (startX, startY)
		self.remainingTiles = (rowDimension * colDimension)
		self.coveredTiles = {(x, y) for x in range(self._rowDimension) for y in range(self._colDimension)}
		self.nonZeroTiles = set()

		self.frontier = []
		

	def inRange(self, i, j):
		return (i >= 0 and i < self._rowDimension) and (j >= 0 and j < self._colDimension)

		

	def getAdjacentCoveredTiles(self, x, y):
		adjacentCoveredTiles = []
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and self.board[i][j] == COVERED:
					adjacentCoveredTiles.append((i, j))

		return adjacentCoveredTiles



	def getNumAdjacentMines(self, x, y):
		mines = 0
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and self.board[i][j] == MINE:
					mines += 1
		return mines



	# Remove guaranteed safe moves from the frontier
	def processSafeMove(self):
		moveX, moveY = self.frontier.pop()
		self.currentMove = (moveX, moveY)
		self.remainingTiles -= 1
		return Action(AI.Action.UNCOVER, moveX, moveY)


	def pushAllAdjacentToFrontier(self, x, y):
		adjacentCovered = self.getAdjacentCoveredTiles(x, y)
		for adjacent in adjacentCovered:
			if adjacent in self.coveredTiles and adjacent not in self.frontier:
				self.frontier.append(adjacent)



	# This function marks a tile as a mine and updates the effective label of all adjacent. If any adjacent tiles becomes 0, then it becomes safe
	def exposeMine(self, x, y, zeroTiles, safeTileFound):
		self.board[x][y] = MINE
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and self.board[i][j] not in labeled:
					self.board[i][j] -= 1
					if(self.board[i][j] == 0 and self.board[i][j] == COVERED and self.board[i][j] not in self.frontier):
						self.frontier.append((i, j))
						zeroTiles.add((i, j))
						safeTileFound = True


	def hiddenMines(self):
		zeroTiles = set()
		safeTileFound = False
		for nonZeroTile in self.nonZeroTiles:
			x, y = nonZeroTile
			coveredTiles = self.getAdjacentCoveredTiles(x, y)
			if(len(coveredTiles) == self.board[x][y]):
				for coveredTile in coveredTiles:
					coveredX, coveredY = coveredTile
					self.exposeMine(coveredX, coveredY, zeroTiles, safeTileFound)
					if safeTileFound:
						break

		for zeroTile in zeroTiles:
			self.nonZeroTiles.remove(zeroTile)

		return safeTileFound
		

	def revealSafe(self):
		for tile in self.coveredTiles:
			x, y = tile
			numHiddenMines = self.getNumAdjacentMines(x, y)
			if(numHiddenMines < self.board[x][y]):
				safeTiles = self.getAdjacentCoveredTiles(x, y)
				for safeTile in safeTiles:
					safeX, safeY = safeTile
					self.pushAllAdjacentToFrontier(safeX, safeY)
				break

	
	def printBoard(self):
		for row in self.board:
			print(row)


		
	def getAction(self, number: int) -> "Action Object":
		# Process newest Move
		if (self.remainingTiles <= self.startingMines):
			return Action(AI.Action.LEAVE)

		currentMoveX, currentMoveY = self.currentMove
		self.board[currentMoveX][currentMoveY] = number - self.getNumAdjacentMines(currentMoveX, currentMoveY)
		self.coveredTiles.remove((currentMoveX, currentMoveY))

		# If the newest move is a 0, then continuously sweep all the 0 mines
		if self.board[currentMoveX][currentMoveY] == 0:
			self.pushAllAdjacentToFrontier(currentMoveX, currentMoveY)
		else:
			self.nonZeroTiles.add((currentMoveX, currentMoveY))

		while True:	
			# Process all safe moves that we know are possible at the moment
			# Should game be over? If so return this
			if (self.remainingTiles <= self.startingMines):
				return Action(AI.Action.LEAVE)
			
			if self.frontier:
				action = self.processSafeMove()
				if action:
					return action
				
				
			# By this point there are no known safe moves, apply rules to learn the safe tiles

			# Rule 1 (Hidden Mines): if effective label matches the number uncovered tiles then all uncovered are mines

			# Returns true if a safe mine was found otherwise we may have gained information on the board
			self.hiddenMines()

			# Rule 2 (Reveal Safe): if effective label matches known adjacent mines, all adjacent covered tiles are safe
			self.revealSafe()


			# Find most probable safe tile (probably by backtracking)


			# Running out of time, make a random move


		"""
		mineX, mineY = self.getMostThreatened()
		self.board[mineX][mineY] = MINE
		self.remainingTiles -= 1
		self.pushAllAdjacentToFrontier(mineX, mineY)
		self.printBoard()
		"""
