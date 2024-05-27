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
COVERED_UNMARKED = 200
UNCOVERED = 300
labeled = [MINE, COVERED_UNMARKED, UNCOVERED]

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
		self.board = [[COVERED_UNMARKED] * self._rowDimension for _ in range(self._colDimension)] 
		self.currentMove = (startX, startY)
		self.remainingTiles = (rowDimension * colDimension)
		self.coveredTiles = {(x, y) for x in range(self._rowDimension) for y in range(self._colDimension)}

		self.uncoveredUnmarkedFrontier = set()
		# self.coveredUnmarkedFrontier = set()

		self.frontier = set()
		
		

	def inRange(self, i, j):
		return (i >= 0 and i < self._rowDimension) and (j >= 0 and j < self._colDimension)

		

	def getAdjacentCoveredUnmarkedTiles(self, x, y):
		adjacentCoveredTiles = []
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and self.board[i][j] == COVERED_UNMARKED:
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
	

	def getLeastThreatenedTile(self):
		# Choose the tile that has the smallest effective label and the most uncovered unmarked tiles around it
		# Safety score = 9 - effectiveLabel + number adjacent uncovered

		bestTiles = None
		bestSafetyScore = 0
		for Tile in self.uncoveredUnmarkedFrontier:
			x, y = Tile
			adjacentCoveredUnmarked = self.getAdjacentCoveredUnmarkedTiles(x, y)
			safetyScore = 9 - self.board[x][y] + len(adjacentCoveredUnmarked)
			if safetyScore > bestSafetyScore:
				bestTiles = adjacentCoveredUnmarked
				bestSafetyScore = safetyScore
		if bestTiles:
			return bestTiles.pop()
		return None



	def processRandomCoveredUnmarked(self):
		leastThreatened = self.getLeastThreatenedTile()
		if leastThreatened:
			moveX, moveY = leastThreatened
			self.currentMove = (moveX, moveY)
			self.remainingTiles -= 1
			return Action(AI.Action.UNCOVER, moveX, moveY)
		else:
			return None
	

	# Random move
	def processRandomCovered(self):
		moveX, moveY = self.coveredTiles.pop()
		self.currentMove = (moveX, moveY)
		self.remainingTiles -= 1
		return Action(AI.Action.UNCOVER, moveX, moveY)



	def pushAllAdjacentToFrontier(self, x, y):
		adjacentCoveredUnmarked = self.getAdjacentCoveredUnmarkedTiles(x, y)
		for adjacent in adjacentCoveredUnmarked:
			if adjacent in self.coveredTiles:
				self.frontier.add(adjacent)


	#def pushAllAdjacentToCoveredUnmarkedFrontier(self, x, y):
	#	adjacentCoveredUnmarked = self.getAdjacentCoveredUnmarkedTiles(x, y)
	#	for adjacent in adjacentCoveredUnmarked:
	#		self.coveredUnmarkedFrontier.add(adjacent)


	# This function marks a tile as a mine and updates the effective label of all adjacent. If any adjacent tiles becomes 0, then it becomes safe
	def exposeMine(self, x, y):
		self.board[x][y] = MINE
		#self.coveredUnmarkedFrontier.remove((x, y))
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and (i, j) in self.uncoveredUnmarkedFrontier:
					self.board[i][j] -= 1
					if(self.board[i][j] == 0):
						self.pushAllAdjacentToFrontier(i, j)




	# If Effective_label(x) == NumUnmarkedNeighbors, then all UnmarkedNeighbors are mines
	def hiddenMines(self):
		mineTiles = None
		for uncoveredUnmarked in self.uncoveredUnmarkedFrontier:
			x, y = uncoveredUnmarked
			coveredTiles = self.getAdjacentCoveredUnmarkedTiles(x, y)
			if(len(coveredTiles) == self.board[x][y]):
				mineTiles = coveredTiles
				break
		
		if mineTiles:
			for mineX, mineY in mineTiles:
				self.exposeMine(mineX, mineY)
		else:
			return True # No information was learned on the board
		

	def revealSafe(self):
		for tile in self.uncoveredUnmarkedFrontier:
			x, y = tile
			if(self.board[x][y] == 0):
				self.uncoveredUnmarkedFrontier.remove((x, y))
				self.pushAllAdjacentToFrontier(x, y)
				return False # Information was found on the board
		return True # No information was added
			


	
	def printBoard(self):
		for row in self.board:
			print(row)


		
	def getAction(self, number: int) -> "Action Object":
		# Process newest Move
		if (len(self.coveredTiles) == self.startingMines):
			return Action(AI.Action.LEAVE)


		currentMoveX, currentMoveY = self.currentMove
		self.board[currentMoveX][currentMoveY] = number - self.getNumAdjacentMines(currentMoveX, currentMoveY)
		
		if self.currentMove in self.coveredTiles:
			self.coveredTiles.remove((currentMoveX, currentMoveY))
		if (len(self.coveredTiles) == self.startingMines):
			return Action(AI.Action.LEAVE)

		#if (currentMoveX, currentMoveY) in self.coveredUnmarkedFrontier:
		#	self.coveredUnmarkedFrontier.remove((currentMoveX, currentMoveY))

		# If the newest move is a 0, then continuously sweep all the 0 mines
		if self.board[currentMoveX][currentMoveY] == 0:
			self.pushAllAdjacentToFrontier(currentMoveX, currentMoveY)
		else:
			self.uncoveredUnmarkedFrontier.add((currentMoveX, currentMoveY))

		#self.printBoard()
		#print(self.currentMove)
		backTrackingNeeded = False
		while True:	

			# Process all safe moves that we know are possible at the moment
			# Should game be over? If so return this
			
			if self.frontier:
				action = self.processSafeMove()
				if action:
					return action
			elif backTrackingNeeded:
				action = self.beginBackTrackingSearch()
				if action:
					return action
				if self.coveredTiles:
					action = self.processRandomCoveredUnmarked()
					if action:
						return action
				return self.processRandomCovered()


			#print(len(self.coveredTiles), self.startingMines)
			if (len(self.coveredTiles) == self.startingMines):
				return Action(AI.Action.LEAVE)
							
			# By this point there are no known safe moves, apply rules to learn the safe tiles


			# Rule 1 (Reveal Safe): if effective label matches known adjacent mines, all adjacent covered tiles are safe
			# Rule 2 (Hidden Mines): if effective label matches the number unmarked tiles then all uncovered are mines
			
			# backTrackingNeeded will be true if both functions reveal no new information about the board
			backTrackingNeeded = self.revealSafe() and self.hiddenMines()


	def beginBackTrackingSearch(self):
		maxTiles = 20
		# V tiles are uncovered
		# C tiles are covered
		V, C, effectiveLabels = self.getVCOrdering(maxTiles)
		n = len(C)

		worldsWhereThisIsAMine = {}
		for neighbor in C:
			for possibleMine in neighbor:
				x, y = possibleMine
				worldsWhereThisIsAMine[(x, y)] = 0

		currentDecisions = []

		self.backTrackingSearch(V, C, effectiveLabels, n - 1, currentDecisions, worldsWhereThisIsAMine)

		leastThreatenedTileThreat = float('inf')
		leastThreatenedTileInAllWorlds = None
		#print(worldsWhereThisIsAMine)
		for tile, threat in worldsWhereThisIsAMine.items():
			if threat < leastThreatenedTileThreat:
				leastThreatenedTileInAllWorlds = tile
				leastThreatenedTileThreat = threat

		if leastThreatenedTileInAllWorlds:
			moveX, moveY = leastThreatenedTileInAllWorlds
			self.currentMove = (moveX, moveY)
			self.remainingTiles -= 1
			return Action(AI.Action.UNCOVER, moveX, moveY)
		
		return None





	def backTrackingSearch(self, V, C, effectiveLabels, i, currentDecisions, worldsWhereThisIsAMine):

		if i == -1: # Constraint satisfied we found a world of possible mines
			for decision in currentDecisions:
				x, y = decision
				worldsWhereThisIsAMine[(x, y)] += 1
			return

		x, y = (V[i][0], V[i][1])
		currentTileEffectiveLabel = effectiveLabels[(x, y)]

		if currentTileEffectiveLabel < 0:
			return
		
		if currentTileEffectiveLabel == 0:
			self.backTrackingSearch(V, C, effectiveLabels, i - 1, currentDecisions, worldsWhereThisIsAMine)
			return
		

		possibleMines = C[i]
		for _ in range(len(possibleMines)):
			if possibleMines and self.changeIsValid(possibleMines[-1], effectiveLabels):
				tryCurrentMine = possibleMines.pop()
				currentDecisions.append(tryCurrentMine)
				self.updateThreats(tryCurrentMine, -1, effectiveLabels)
				self.backTrackingSearch(V, C, effectiveLabels, i, currentDecisions, worldsWhereThisIsAMine)
				self.updateThreats(tryCurrentMine, 1, effectiveLabels)	
				currentDecisions.pop()
				possibleMines.insert(0, tryCurrentMine)



	def updateThreats(self, tryCurrentMine, change, effectiveLabels):
		x, y = tryCurrentMine
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if (i, j) in effectiveLabels:
					effectiveLabels[(i, j)] += change

	def changeIsValid(self, tryCurrentMine, effectiveLabels):
		x, y = tryCurrentMine
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if (i, j) in effectiveLabels and effectiveLabels[(i, j)] == 0:
					return False
		return True




	def getVCOrdering(self, maxTiles):
		selectedTiles = []
		V = []
		C = []

		effectiveLabels = {}
		for tile in self.uncoveredUnmarkedFrontier:
			x, y = tile
			safetyScore, adjacentCovered = self.getSafetyScoreAndAdjacentCovered(x, y)
			# coordinate, safety score, covered tiles adjacent
			selectedTiles.append(((x, y), safetyScore, adjacentCovered))
		
		selectedTiles = sorted(selectedTiles, key=lambda x:x[1] , reverse=True)
		n = min(maxTiles, len(selectedTiles))

		for i in range(n):
			C.append(selectedTiles[i][2])
			V.append(selectedTiles[i][0])
			x, y = selectedTiles[i][0]
			effectiveLabels[(x, y)] = self.board[x][y]

		return V, C, effectiveLabels


		
	
	def getAdjacentCoveredFrontierTiles(self, x, y):
		adjacentCoveredTiles = []
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and self.board[i][j] == COVERED_UNMARKED:
					adjacentCoveredTiles.append((i, j))
		return adjacentCoveredTiles

	
	def getSafetyScoreAndAdjacentCovered(self, x, y):
		adjacentUncovered = self.getAdjacentCoveredFrontierTiles(x, y)
		safetyScore = (9 - self.board[x][y]) + len(adjacentUncovered)
		return safetyScore, adjacentUncovered
