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

import math
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
		self.numMinesLeft = totalMines # keep track of how many mines are left in the game
		self.numStartingMines = totalMines # Constant: the number of mines we started with
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
		self.frontier_covered_safe = set()   	# list of safe tiles to be uncovered
		self.mines = set() # list of mines to be flagged
		self.numConsecutiveLoopThatDoNothing = 0
		

	def inRange(self, i, j):
		return (i >= 0 and i < self._rowDimension) and (j >= 0 and j < self._colDimension)


	def get_frontier_uncovered(self):
		# Check each tile on the board, if it is uncovered and has at least 1 covered tile around -> it should be in the frontier_uncovered
		frontier_uncovered = set()
		for row in range(self._rowDimension):
			for col in range(self._colDimension):
				if 0<= self.board[row][col] <= 8: # 8 is the max number of mine around a tile, the effective lable <= 8 means the tile is uncovered and is not mine/flagged
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
					if (self.board[i][j] == MINE or self.board[i][j] == -1): # MINE denotes unflagged mines, -1 is flagged mines
						numMines += 1
					elif(self.board[i][j] == COVERED_UNKNOWN or self.board[i][j] == COVERED_SAFE):
						coveredTiles.add((i, j))
		return numMines, coveredTiles


	def getAdjacentUncovered(self, x, y):
		uncoveredTiles = set()
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):
				if self.inRange(i, j) and (i, j) != (x, y) and 0 <= self.board[i][j] <= 8:
					uncoveredTiles.add((i, j))
		return uncoveredTiles

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
								self.frontier_covered_safe.append(coveredTile)
		




	def updateBoardNewMove(self, number):
		x, y = self.prevMove

		# numAdjacentMines is the number of known mines so far, covered tiles are all adjacent covered tiles that are not bombs
		numAdjacentMines, coveredTiles = self.getNumAdjacentMinesAndCovered(x, y)

		# if not mine, compute effective label by taking its hint number and subtracing all known mines around it
		if number != -1: 
			self.board[x][y] = number - numAdjacentMines
		else:
			self.board[x][y] = number
			

		# if the effective label is equal to the number of covered tiles then all uncovered tiles are mines
		if self.board[x][y] == len(coveredTiles):
			for i, j in coveredTiles:
				self.board[i][j] = MINE
				self.numMinesLeft -= 1	
				self.mines.add((i,j))

		# if the hint number is equal to the number of mines we are aware of or if it's 0, then the rest must be safe
		if number == 0 or number == numAdjacentMines:
			for i, j in coveredTiles:
				if self.board[i][j] != COVERED_SAFE:
					self.board[i][j] = COVERED_SAFE
					self.frontier_covered_safe.add((i, j))




	def print_status(self):
		# Transpose the array
		transposed_array = list(zip(*self.board))

		# Reverse each row
		rotated_array = [list(row)[::-1] for row in transposed_array]

		# Reverse the order of the rows
		rotated_array.reverse()
  
		# Print out the rotated board
		for row in rotated_array:
			print(row[::-1])
  
   
		modified_frontier_uncovered = set()
		modified_frontier_covered = set()
		modified_frontier_covered_safe = set()
		modified_mines = set()

		for tuple_pair in self.frontier_uncovered:
			modified_tuple = tuple(x + 1 for x in tuple_pair)
			modified_frontier_uncovered.add(modified_tuple)
		for tuple_pair in self.frontier_covered:
			modified_tuple = tuple(x + 1 for x in tuple_pair)
			modified_frontier_covered.add(modified_tuple)
		for tuple_pair in self.frontier_covered_safe:
			modified_tuple = tuple(x + 1 for x in tuple_pair)
			modified_frontier_covered_safe.add(modified_tuple)
		for tuple_pair in self.mines:
			modified_tuple = tuple(x + 1 for x in tuple_pair)
			modified_mines.add(modified_tuple)
   

   
		print("Frontier_uncovered: ", modified_frontier_uncovered)
		print("frontier_covered: ", modified_frontier_covered)
		print("frontier_covered_safe: ", modified_frontier_covered_safe)
		print("mines: ", modified_mines)
		print("Num covered tiles: ", self.remainingTiles)
		print("Num covered, unflagged tiles: ", self.numCoveredUnflaggedTiles)
		print("Num flagged tiles: ", self.numFlaggedTiles)
		print("\n")

		
	def getAction(self, number: int) -> "Action Object":
		self.updateBoardNewMove(number)

		if self.numCoveredUnflaggedTiles == self.numMinesLeft:
			for x in range(self._rowDimension):
				for y in range(self._colDimension):
					if self.board[x][y] > 8:
						self.numMinesLeft -= 1	
						self.mines.add((x,y))

		# If the game is over -> uncover all remaining tiles and leave (no more tiles left to uncover)
		if (self.numFlaggedTiles == self.numStartingMines):
			for x in range(self._rowDimension):
				for y in range(self._colDimension):
					if self.board[x][y] == COVERED_UNKNOWN:
						self.board[x][y] = COVERED_SAFE # update board
						self.frontier_covered_safe.add((x,y))

		# if uncovered/flagged all tiles -> leave game
		if self.numCoveredUnflaggedTiles == 0:
			# self.print_status()
			# print("No more covered unflagged tile, Leaving game")
			self.numConsecutiveLoopThatDoNothing = 0 # reset this variable
			return Action(AI.Action.LEAVE)

		
		self.frontier_uncovered = self.get_frontier_uncovered()
		self.frontier_covered = self.get_frontier_covered()
		# self.print_status()

		# uncover all tiles in frontier_covered_safe
		if self.frontier_covered_safe:
			moveX, moveY = self.frontier_covered_safe.pop()
			self.prevMove = (moveX, moveY)
			self.prevAction = AI.Action.UNCOVER
			self.remainingTiles -= 1
			self.numCoveredUnflaggedTiles -=1
			self.numConsecutiveLoopThatDoNothing = 0 # reset this variable
			return Action(AI.Action.UNCOVER, moveX, moveY)

		# if frontier_covered_safe is empty, it means no safe tile left -> start flagging known mines
		elif self.mines: 
			flagX, flagY = self.mines.pop()
			self.prevMove = (flagX, flagY)
			self.prevAction = AI.Action.FLAG
			self.numCoveredUnflaggedTiles -=1
			self.numFlaggedTiles += 1
			self.board[flagX][flagY] = MINE
			# update board
			for i in range(flagX - 1, flagX + 2):
				for j in range(flagY - 1, flagY + 2):
					if self.inRange(i, j) and (i, j) != (flagX, flagY) and 1 <= self.board[i][j] <= 8:
						self.board[i][j] -= 1
			self.numConsecutiveLoopThatDoNothing = 0 # reset this variable
			return Action(AI.Action.FLAG, flagX, flagY)
		
 		# else, start checking for unknown mines		
		else:
			# scan frontier_uncovered to see if effective number of a tile == number of covered tiles around it, then all covered tiles around it are mines
			for x, y in self.frontier_uncovered:
				numAdjacentMines, coveredTiles = self.getNumAdjacentMinesAndCovered(x, y)
				if self.board[x][y] == len(coveredTiles):
					for i, j in coveredTiles:
						if self.board[i][j] == COVERED_UNKNOWN:
							self.numMinesLeft -= 1	
							self.mines.add((i,j))
								
			# if no mine has been detected, scan frontier_covered and use probability to detect mines
			if (len(self.mines) == 0):
				probability = dict()
				for tile_x, tile_y in self.frontier_covered:
					# add all effective numbers of uncovered tiles around it
					adjacenUncoveredTiles = self.getAdjacentUncovered(tile_x, tile_y)
					for xcoor, ycoor in adjacenUncoveredTiles:
						sum = self.board[xcoor][ycoor]
						if sum == 0:
							probability[(tile_x, tile_y)] = 0
							break
						if (probability.get((tile_x, tile_y))):
							probability[(tile_x, tile_y)] += sum
						else: 
							probability[(tile_x, tile_y)] = sum

				# get the tile with lowest chance of being mine, and add it to the frontier_covered_safe
				if (len(probability) != 0):
					tile_with_min_mine_probability = min(probability, key=probability.get)
					

					if probability[tile_with_min_mine_probability] == 0:
						# add all tiles with 0 probability of mine to frontier_covered_safe
						for key, value in probability.items():
							if value == 0:
								self.frontier_covered_safe.add(key)
        
					elif self.numConsecutiveLoopThatDoNothing > 1: 
						# if all covered tiles have only 1 unique value -> uncover a tile farthest from to center
						max_distance_to_center = 0
						tile_farthest_from_center = None
						for key, value in probability.items():
							x, y = key
							distance_to_center = math.sqrt((x - 3)**2 + (y - 3)**2) # center of board is (3,3)
							if distance_to_center > max_distance_to_center:
								max_distance_to_center = distance_to_center
								tile_farthest_from_center = (x,y)
						self.frontier_covered_safe.add(tile_farthest_from_center)
		
					# print out probability
					modified_probability = dict() # use modified_probability to print out
					for key, value in probability.items():
						modified_key = tuple(x + 1 for x in key)
						# Add the modified key-value pair to the new dictionary
						modified_probability[modified_key] = value

					# print("probability: ", modified_probability)
     

		


		prev_X, prev_Y = self.prevMove
		# print("Do nothing in this loop --- previous action: ", self.prevAction, " --- previous (x,y): ", (prev_X, prev_Y))
		self.numConsecutiveLoopThatDoNothing += 1
		return Action(self.prevAction, prev_X, prev_Y) # means do nothing




					
		
		


		
				






		




		
        

