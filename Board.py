import math
import copy



class Board:
	pieces = [
	    ('Empty', 'No Color'), ('Pawn', 'Black'), ('Knight', 'Black'), ('Bishop', 'Black'), ('Rook', 'Black'), ('Queen', 'Black'), ('King', 'Black'), 
	    ('Pawn', 'White'), ('Knight', 'White'), ('Bishop', 'White'), ('Rook', 'White'), ('Queen', 'White'), ('King', 'White')
	]

	grid = [0]*8
	for i in range(len(grid)):
		grid[i]=[0]*8
	viableSpaces = []
	
	
	def __init__(self):
		self.grid[1] = [1]*8
		self.grid[6] = [7]*8
		self.grid[0][0] = 4
		self.grid[0][1] = 2
		self.grid[0][2] = 3
		self.grid[0][3] = 5
		self.grid[0][4] = 6
		self.grid[0][5] = 3
		self.grid[0][6] = 2
		self.grid[0][7] = 4
		self.grid[7][0] = 10
		self.grid[7][1] = 8
		self.grid[7][2] = 9
		self.grid[7][3] = 11
		self.grid[7][4] = 12
		self.grid[7][5] = 9
		self.grid[7][6] = 8
		self.grid[7][7] = 10
		

	def moveValid(self, grid, curPos, finPos):
		ID = grid[curPos[0]][curPos[1]]%6
		#Pawn rules ___________________________________________________________________________________________
		if ID == 1:
			if self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black':
				if grid[finPos[0]][finPos[1]] == 0 and [curPos[0]+1, curPos[1]] == [finPos[0], finPos[1]]:
					return True
				#Black: Moving two spaces foward
				elif curPos[0] == 1 and \
				    [curPos[0]+2, curPos[1]] == [finPos[0], finPos[1]] and grid[curPos[0]+1][curPos[1]] == 0 and grid[finPos[0]][finPos[1]] == 0:
					return True
				#Black: Attacking
				elif grid[finPos[0]][finPos[1]] != 0 and ([curPos[0]+1, curPos[1]-1] == [finPos[0], finPos[1]] or \
				    [curPos[0]+1, curPos[1]+1] == [finPos[0], finPos[1]]) and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'White':
					return True
			else:
				if grid[finPos[0]][finPos[1]] == 0 and [curPos[0]-1, curPos[1]] == [finPos[0], finPos[1]]:
					return True
				#White: Moving two spaces foward
				elif curPos[0] == 6 and [curPos[0]-2, curPos[1]] == [finPos[0], finPos[1]] and grid[curPos[0]-1][curPos[1]] == 0 and \
				    grid[finPos[0]][finPos[1]] == 0:
					return True
				#White: Attacking
				elif grid[finPos[0]][finPos[1]] != 0 and ([curPos[0]-1, curPos[1]-1] == [finPos[0], finPos[1]] or \
					[curPos[0]-1, curPos[1]+1] == [finPos[0], finPos[1]]) and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'Black':
					return True

		#Knight rules ___________________________________________________________________________________________
		elif ID == 2:
			distance = math.sqrt((finPos[0]-curPos[0])**2 + (finPos[1]-curPos[1])**2)
			if grid[finPos[0]][finPos[1]] == 0 and distance == 2.23606797749979:
				return True
			#Black: Attacking
			elif grid[finPos[0]][finPos[1]] != 0 and distance == 2.23606797749979 and \
			    self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black' and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'White':
				return True
			#White: Attacking
			elif grid[finPos[0]][finPos[1]] != 0 and distance == 2.23606797749979 and \
			    self.pieces[grid[curPos[0]][curPos[1]]][1] == 'White' and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'Black':
				return True

		#Bishop rules ___________________________________________________________________________________________
		elif ID == 3:
			if self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black':
				color = 'White'
			elif self.pieces[grid[curPos[0]][curPos[1]]][1] == 'White':
				color = 'Black'
			else:
				color = 'No Color'
			self.viableSpaces = []
			for i in range(4):
				self.detViableDiagSpaces(grid, curPos, i, color)
			if finPos in self.viableSpaces:
				return True

		#Rook rules ___________________________________________________________________________________________
		elif ID == 4:
			if self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black':
				color = 'White'
			elif self.pieces[grid[curPos[0]][curPos[1]]][1] == 'White':
				color = 'Black'
			else:
				color = 'No Color'
			self.viableSpaces = []
			for i in range(4):
				self.detViableHorizVertSpaces(grid, curPos, i, color)
			if finPos in self.viableSpaces:
				return True

		#Queen rules ___________________________________________________________________________________________
		elif ID == 5:
			if self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black':
				color = 'White'
			elif self.pieces[grid[curPos[0]][curPos[1]]][1] == 'White':
				color = 'Black'
			else:
				color = 'No Color'
			self.viableSpaces = []
			for i in range(4):
				self.detViableHorizVertSpaces(grid, curPos, i, color)
				self.detViableDiagSpaces(grid, curPos, i, color)
			if finPos in self.viableSpaces:
				return True

		#King rules ___________________________________________________________________________________________
		elif ID == 0:
			if grid[curPos[0]][curPos[1]] != 0:
				distance = math.sqrt((finPos[0]-curPos[0])**2 + (finPos[1]-curPos[1])**2)
				if grid[finPos[0]][finPos[1]] == 0 and distance < 1.5:
					return True
				#Black: Attacking
				elif grid[finPos[0]][finPos[1]] != 0 and distance < 1.5 and \
				    self.pieces[grid[curPos[0]][curPos[1]]][1] == 'Black' and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'White':
					return True
				#White: Attacking
				elif grid[finPos[0]][finPos[1]] != 0 and distance < 1.5 and \
				    self.pieces[grid[curPos[0]][curPos[1]]][1] == 'White' and self.pieces[grid[finPos[0]][finPos[1]]][1] == 'Black':
					return True
		return False
		

	def detViableDiagSpaces(self, grid, curPos, i, color):
		if i == 0:
			try:
				if grid[curPos[0]+1][curPos[1]+1] != 0 and self.pieces[grid[curPos[0]+1][curPos[1]+1]][1] != color:
					pass
				else:
					newPos = [curPos[0]+1, curPos[1]+1]
					if newPos[0] >= 0 and newPos[1] >= 0:
						self.viableSpaces.append(newPos)
						if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
							self.detViableDiagSpaces(grid, newPos, i, color)
			except:
				pass

		elif i == 1:
			try:
				if grid[curPos[0]+1][curPos[1]-1] != 0 and self.pieces[grid[curPos[0]+1][curPos[1]-1]][1] != color:
					pass
				else:
					newPos = [curPos[0]+1, curPos[1]-1]
					if newPos[0] >= 0 and newPos[1] >= 0:
						self.viableSpaces.append(newPos)
						if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
							self.detViableDiagSpaces(grid, newPos, i, color)
			except:
				pass
		elif i == 2:
			try:
				if grid[curPos[0]-1][curPos[1]+1] != 0 and \
				    self.pieces[grid[curPos[0]-1][curPos[1]+1]][1] != color:
					pass
				else:
					newPos = [curPos[0]-1, curPos[1]+1]
					if newPos[0] >= 0 and newPos[1] >= 0:
						self.viableSpaces.append(newPos)
						if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
							self.detViableDiagSpaces(grid, newPos, i, color)
			except:
				pass
		else:
			try:
				if grid[curPos[0]-1][curPos[1]-1] != 0 and \
				    self.pieces[grid[curPos[0]-1][curPos[1]-1]][1] != color:
					pass
				else:
					newPos = [curPos[0]-1, curPos[1]-1]
					if newPos[0] >= 0 and newPos[1] >= 0:
						self.viableSpaces.append(newPos)
						if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
							self.detViableDiagSpaces(grid, newPos, i, color)
			except:
				pass


	def detViableHorizVertSpaces(self, grid, curPos, i, color):
			if i == 0:
				try:
					if grid[curPos[0]+1][curPos[1]] != 0 and \
					    self.pieces[grid[curPos[0]+1][curPos[1]]][1] != color:
						pass
					else:
						newPos = [curPos[0]+1, curPos[1]]
						if newPos[0] >= 0 and newPos[1] >= 0:
							self.viableSpaces.append(newPos)
							if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
								self.detViableHorizVertSpaces(grid, newPos, i, color)
				except:
					pass

			elif i == 1:
				try:
					if grid[curPos[0]-1][curPos[1]] != 0 and self.pieces[grid[curPos[0]-1][curPos[1]]][1] != color:
						pass
					else:
						newPos = [curPos[0]-1, curPos[1]]
						if newPos[0] >= 0 and newPos[1] >= 0:
							self.viableSpaces.append(newPos)
							if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
								self.detViableHorizVertSpaces(grid, newPos, i, color)
				except:
					pass

			elif i == 2:
				try:
					if grid[curPos[0]][curPos[1]+1] != 0 and self.pieces[grid[curPos[0]][curPos[1]+1]][1] != color:
						pass
					else:
						newPos = [curPos[0], curPos[1]+1]
						if newPos[0] >= 0 and newPos[1] >= 0:
							self.viableSpaces.append(newPos)
							if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
								self.detViableHorizVertSpaces(grid, newPos, i, color)
				except:
					pass

			else:
				try:
					if grid[curPos[0]][curPos[1]-1] != 0 and \
					    self.pieces[grid[curPos[0]][curPos[1]-1]][1] != color:
						pass
					else:
						newPos = [curPos[0], curPos[1]-1]
						if newPos[0] >= 0 and newPos[1] >= 0:
							self.viableSpaces.append(newPos)
							if self.pieces[grid[newPos[0]][newPos[1]]][1] != color:
								self.detViableHorizVertSpaces(grid, newPos, i, color)
				except:
					pass
					

	def detPonSpaces(self, grid, curPos, color):
		ponSpaces = []
		if color == "Black":
			if 0 <= curPos[0]+1 < 8 and grid[curPos[0]+1][curPos[1]] == 0:
				ponSpaces.append([curPos[0]+1, curPos[1]])
			if 0 <= curPos[0]+2 < 8 and \
			    grid[curPos[0]+2][curPos[1]] == 0 and curPos[0] == 1 and grid[curPos[0]+1][curPos[1]] == 0:
				ponSpaces.append([curPos[0]+2, curPos[1]])
			if 0 <= curPos[0]+1 < 8 and 0 <= curPos[1]+1 < 8 and \
			    self.pieces[grid[curPos[0]+1][curPos[1]+1]][1] == "White":
				ponSpaces.append([curPos[0]+1, curPos[1]+1])
			if 0 <= curPos[0]+1 < 8 and 0 <= curPos[1]-1 < 8 and \
			    self.pieces[grid[curPos[0]+1][curPos[1]-1]][1] == "White":
				ponSpaces.append([curPos[0]+1, curPos[1]-1])
			return ponSpaces

		elif color == "White":
			if 0 <= curPos[0]-1 < 8 and grid[curPos[0]-1][curPos[1]] == 0:
				ponSpaces.append([curPos[0]-1, curPos[1]])
			if 0 <= curPos[0]-2 < 8 and \
		        grid[curPos[0]-2][curPos[1]] == 0 and curPos[0] == 6 and grid[curPos[0]-1][curPos[1]] == 0:
				ponSpaces.append([curPos[0]-2, curPos[1]])
			if 0 <= curPos[0]-1 < 8 and 0 <= curPos[1]+1 < 8 and \
			    self.pieces[grid[curPos[0]-1][curPos[1]+1]][1] == "Black":
				ponSpaces.append([curPos[0]-1, curPos[1]+1])
			if 0 <= curPos[0]-1 < 8 and 0 <= curPos[1]-1 < 8 and \
			    self.pieces[grid[curPos[0]-1][curPos[1]-1]][1] == "Black":
				ponSpaces.append([curPos[0]-1, curPos[1]-1])
			return ponSpaces
			

	def detKnightSpaces(self, grid, curPos, color):
		return [
		    [curPos[0]+2, curPos[1]+1], 
		    [curPos[0]+2, curPos[1]-1], 
		    [curPos[0]+1, curPos[1]+2], 
		    [curPos[0]+1, curPos[1]-2], 
		    [curPos[0]-1, curPos[1]+2], 
		    [curPos[0]-1, curPos[1]-2], 
		    [curPos[0]-2, curPos[1]+1], 
		    [curPos[0]-2, curPos[1]-1]
		]
		

	def detBishopSpaces(self, grid, curPos, color):
		self.viableSpaces = []
		for i in range(4):
			self.detViableDiagSpaces(grid, curPos, i, color)
		return self.viableSpaces
		

	def detRookSpaces(self, grid, curPos, color):
		self.viableSpaces = []
		for i in range(4):
			self.detViableHorizVertSpaces(grid, curPos, i, color)
		return self.viableSpaces
		

	def detQueenSpaces(self, grid, curPos, color):
		self.viableSpaces = []
		for i in range(4):
			self.detViableDiagSpaces(grid, curPos, i, color)
			self.detViableHorizVertSpaces(grid, curPos, i, color)
		return self.viableSpaces
		

	def detKingSpaces(self, grid, curPos, color):
		return [
		    [curPos[0]+1, curPos[1]],
		    [curPos[0], curPos[1]+1], 
		    [curPos[0]-1, curPos[1]], 
		    [curPos[0], curPos[1]-1], 
		    [curPos[0]+1, curPos[1]+1], 
		    [curPos[0]-1, curPos[1]+1], 
		    [curPos[0]+1, curPos[1]-1], 
		    [curPos[0]-1, curPos[1]-1]
	    ]
					


	def inCheck(self,  grid,  color):
		for r in range(len(grid)):
			for p in range(len(grid[r])):
				if grid[r][p] != 0 and grid[r][p]%6 == 0 and \
				self.pieces[grid[r][p]][1] == color:
				    kingPos = [r, p]
		for r in range(len(grid)):
			for p in range(len(grid[r])):
				if grid[r][p] != 0 and \
				self.pieces[grid[r][p]][1] != color:
					if self.moveValid(grid, [r, p], kingPos):
						return True
		return False
	

	def turnValid(self, grid, curPos, finPos, color):
		bool = self.moveValid(grid, curPos, finPos)
		if bool:
#			temp = [0]*8
#			for i in range(len(temp)):
#				temp[i]=grid[i][:]
			temp = copy.deepcopy(grid)
			temp[finPos[0]][finPos[1]] = temp[curPos[0]][curPos[1]]
			temp[curPos[0]][curPos[1]] = 0
			if not self.inCheck(temp, color):
				return True
		return False