import math
import Board as cb
from random import choice
import copy



class Computer:
	
	def makeMove(self,guiBoard,color):
#		temp = [0]*8
#		for i in range(len(temp)):
#			temp[i]=guiBoard.grid[i][:]
		temp = copy.deepcopy(guiBoard.grid)
		if color == "Black":
			antiColor = "White"
		else:
			antiColor = "Black"
			
		first = self.simulateTurn(temp,color,guiBoard)[:]
		for fmove in first:
			fmove[4] = self.simulateTurn(fmove[0],antiColor,guiBoard)[:]
			for smove in fmove[4]:
				smove[4] = self.simulateTurn(smove[0],color,guiBoard)[:]
		
		for f in first:
			maxVal2 = -100
			for g in f[4]:
				maxVal3 = 0
				for h in g[4]:
					if h[3] > maxVal3:
						maxVal3 = h[3]
				g[3] = g[3] - maxVal3
				if g[3] > maxVal2:
					maxVal2 = g[3]
			f[3] = f[3] - maxVal2
		
		bestMoves = []
		maxValue = 0
		for v in first:
			if v[3] > maxValue:
				bestMoves = []
				bestMoves.append(v)
				maxValue = v[3]
			elif v[3] == maxValue:
				bestMoves.append(v)
#		for b in bestMoves:
#			print(b[1],b[2],b[3])
		try:
			return choice(bestMoves)
		except:
			return choice(first)
		

	def simulateTurn(self,temp,color,guiBoard):
		if color == "Black":
			antiColor = "White"
		else:
			antiColor = "Black"
		
		self.myPieces = [] # location, value
		for r in range(len(temp)):
			for c in range(len(temp[r])):
				if temp[r][c] != 0:
					if color == guiBoard.pieces[temp[r][c]][1]:
						self.myPieces.append([[r,c],temp[r][c]])
		
		validMoves = []
		for p in self.myPieces:
			if p[1]%6 == 1:
				possibleMoves = guiBoard.detPonSpaces(temp,p[0],color)[:]
			elif p[1]%6 == 2:
				possibleMoves = guiBoard.detKnightSpaces(temp,p[0],color)[:]
			elif p[1]%6 == 3:
				possibleMoves = guiBoard.detBishopSpaces(temp,p[0],antiColor)[:]
			elif p[1]%6 == 4:
				possibleMoves = guiBoard.detRookSpaces(temp,p[0],antiColor)[:]
			elif p[1]%6 == 5:
				possibleMoves = guiBoard.detQueenSpaces(temp,p[0],antiColor)[:]
			else:
				possibleMoves = guiBoard.detKingSpaces(temp,p[0],color)[:]
				
			for m in possibleMoves:
				if p[1]%6 == 2 or p[1]%6 == 0:
					if 0 <= m[0] < 8 and  0 <= m[1] < 8 and guiBoard.turnValid(temp,p[0],m,color):
						moveGrid = [0]*8
						for i in range(len(moveGrid)):
							moveGrid[i] = temp[i][:]
						value = moveGrid[m[0]][m[1]]%6
						if guiBoard.inCheck(moveGrid,color):
							value += 3
						moveGrid[m[0]][m[1]] = p[1]; moveGrid[p[0][0]][p[0][1]] = 0
						if guiBoard.inCheck(moveGrid,antiColor):
							value += 3
						validMoves.append([moveGrid,p[0],m,value,[]])
						
				else:
#					moveGrid = [0]*8
#					for i in range(len(moveGrid)):
#						moveGrid[i] = temp[i][:]
					moveGrid = copy.deepcopy(temp)
					value = moveGrid[m[0]][m[1]]%6
					if guiBoard.inCheck(moveGrid,color):
						value += 3
					moveGrid[m[0]][m[1]] = p[1]; moveGrid[p[0][0]][p[0][1]] = 0
					if not guiBoard.inCheck(moveGrid,color):
						if guiBoard.inCheck(moveGrid,antiColor):
							value += 3
						if p[1]%6 == 1 and (m[0] == 8 or m[0] == 0):
							value += 5
						validMoves.append([moveGrid,p[0],m,value,[]])

		return validMoves	
					
				