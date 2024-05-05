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
SAFE = 300
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
		self.prevMove = (startX, startY)
		self.remainingTiles = (rowDimension * colDimension)


		self.uncoveredTiles = set()
		#print(self.uncoveredTiles)
		self.frontier = []
		

	def inRange(self, i, j):
		return (i >= 0 and i < self._rowDimension) and (j >= 0 and j < self._colDimension)

		

	def getNumAdjacentMinesAndCovered(self, x, y):
		numMines = 0
		coveredTiles = []
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j):
					if (self.board[i][j] == MINE):
						numMines += 1
					elif(self.board[i][j] == COVERED):
						coveredTiles.append((i, j))

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
							if self.board[coveredX][coveredY] != SAFE:
								self.board[coveredX][coveredY] = SAFE
								self.frontier.append(coveredTile)
		



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


		# if the hint number is equal to the number of mines we are aware of or if it's 0, then the rest must be safe
		if number == 0 or number == numAdjacentMines:
			for i, j in coveredTiles:
				if self.board[i][j] != SAFE:
					self.board[i][j] = SAFE
					self.frontier.append((i, j))


	def updateBoardExistingTiles(self, move):
		x, y = move
		numAdjacentMines, coveredTiles = self.getNumAdjacentMinesAndCovered(x, y)

		# if the effective label is equal to the number of covered tiles then all uncovered tiles are mines
		#print(self.board[x][y])
		if self.board[x][y] == len(coveredTiles):
			for i, j in coveredTiles:
				self.board[i][j] = MINE
				self._totalMines -= 1	


		# if the hint number is equal to the number of mines we are aware of or if it's 0, then the rest must be safe
		if self.board[x][y] == 0 or self.board[x][y] == numAdjacentMines:
			for i, j in coveredTiles:
				if self.board[i][j] != SAFE:
					self.board[i][j] = SAFE
					self.frontier.append((i, j))



		
	def getAction(self, number: int) -> "Action Object":
		# If the game is over leave (no more tiles left to uncover)
		if (self.remainingTiles <= self.startingMines):
			return Action(AI.Action.LEAVE)
		
		self.updateBoardNewMove(number)
		#for row in self.board:
		#	print(row)

		if self.frontier:
			moveX, moveY = self.frontier.pop()
			self.prevMove = (moveX, moveY)
			self.remainingTiles -= 1
			return Action(AI.Action.UNCOVER, moveX, moveY)
		
		


		
				






		




		
        

