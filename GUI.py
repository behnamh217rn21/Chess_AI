import sys
import os

try:
	import tkinter as tk
	from tkinter import *
except:
	import Tkinter as tk
	from Tkinter import *
import Board as cb
import Computer as com



class App:
    board = cb.Board()
    t = 0
    itemClicked = True
    comOp = False
    colors = ['White', 'Black']
    missingPiecesBlack = []
    missingPiecesWhite = []
	
    def __init__(self, master, mode):
        self.mode = mode
        self.Master = master
        master.title("Chess")
        self.canvas = Canvas(self.Master)
        self.isStopped = True
        self.pieces = [
            tk.PhotoImage(file = 'pieces_image/SquareWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/PawnBlack.gif'), 
            tk.PhotoImage(file = 'pieces_image/KnightBlack.gif'), 
            tk.PhotoImage(file = 'pieces_image/BishopBlack.gif'),  
            tk.PhotoImage(file = 'pieces_image/RookBlack.gif'), 
            tk.PhotoImage(file = 'pieces_image/QueenBlack.gif'), 
            tk.PhotoImage(file = 'pieces_image/KingBlack.gif'), 
            tk.PhotoImage(file = 'pieces_image/PawnWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/KnightWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/BishopWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/RookWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/QueenWhite.gif'),  
            tk.PhotoImage(file = 'pieces_image/KingWhite.gif')
        ]
        self.activePieces = [
            tk.PhotoImage(file = 'pieces_image/SquareWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/PawnBlackAct.gif'), 
            tk.PhotoImage(file = 'pieces_image/KnightBlackAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/BishopBlackAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/RookBlackAct.gif'), 
            tk.PhotoImage(file = 'pieces_image/QueenBlackAct.gif'), 
            tk.PhotoImage(file = 'pieces_image/KingBlackAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/PawnWhiteAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/KnightWhiteAct.gif'), 
            tk.PhotoImage(file = 'pieces_image/BishopWhiteAct.gif'), 
            tk.PhotoImage(file = 'pieces_image/RookWhiteAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/QueenWhiteAct.gif'),  
            tk.PhotoImage(file = 'pieces_image/KingWhiteAct.gif')
        ]
        self.emptySpaces = [
            tk.PhotoImage(file = 'pieces_image/SquareWhite.gif'), 
            tk.PhotoImage(file = 'pieces_image/SquareGrey.gif'), 
            tk.PhotoImage(file = 'pieces_image/SquareActive.gif'),  
            tk.PhotoImage(file = 'pieces_image/SquareClicked.gif')
        ]

        # Adding Top Menu
        self.menu_bar = Menu(self.Master)
        self.file_menu = Menu(self.menu_bar, tearoff = 0)
        # add a submenu
        sub_menu = Menu(self.file_menu, tearoff = 0)

        sub_menu.add_command(
        	label = 'Human vs Human', command = lambda: [self.canvas.delete(ALL), self.Master.destroy(), os.system("python GUI.py Human_Human")]
        )
        sub_menu.add_command(
        	label = 'AI vs Human', command = lambda: [self.canvas.delete(ALL), self.Master.destroy(), os.system("python GUI.py AI_Human")]
        )
        sub_menu.add_command(
        	label = 'AI vs AI', command = lambda: [self.canvas.delete(ALL), self.Master.destroy(), os.system("python GUI.py AI_AI")]
        )

        # add the File menu to the menu_bar
        self.file_menu.add_cascade(
            label = "New Game", menu = sub_menu
        )
        # add Exit menu item
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Exit', command = lambda: [self.canvas.delete(ALL), self.Master.destroy(), self.stop()])

        self.menu_bar.add_cascade(
            label = "Menu", menu = self.file_menu
        )

        self.Master.config(menu = self.menu_bar)
        self.frame = Frame(master); self.frame.grid()

        if self.mode  ==  'Human_Human':
        	self.frame.destroy()
        	self.startGame()
        else:
            self.comOp = True
            self.computer = com.Computer()
            self.frame.destroy()
            self.startGame()
		

    def stop(self): 
        # Stop animation
        self.isStopped = not(self.isStopped)

    def startGame(self):
        self.Master.minsize(778, 782) #Width,  height
        self.canvas.config(height = 782, width = 778, bg = 'black')
        self.canvas.pack()
        self.Master.update()
        self.displayBoard()
		
    def displayBoard(self):
        for i in range(8):
            for j in range(8):
                lW = 10 + 96*i
                lH = 10 + 96*j
                self.canvas.create_image(
                	lW, lH, image = self.emptySpaces[(i+j)%2], anchor = NW, activeimage = self.emptySpaces[2]
                )
        for r in range(8):
            for c in range(8):
                lH = 10 + 96*r
                lW = 10 + 96*c
                if self.board.grid[r][c] !=  0:
                    self.canvas.create_image(
                    	lW, lH, image = self.pieces[self.board.grid[r][c]], anchor = NW, activeimage = self.activePieces[self.board.grid[r][c]]
                    )
        for k in range(12):
            lH = 10 + 61*k
            self.canvas.create_image(
            	779, lH, image = self.emptySpaces[0], anchor = NW
            )
        for l in range(len(self.missingPiecesBlack)):
            lH = 10 + 96*l
            self.canvas.create_image(
            	779, lH, image = self.pieces[self.missingPiecesBlack[l]], anchor = NW
            )
        for n in range(len(self.missingPiecesWhite)):
            lH = 394 + 96*n
            self.canvas.create_image(
            	779, lH, image = self.pieces[self.missingPiecesWhite[n]], anchor = NW
            )
        self.Master.update()
		
    def callback(self, event):
        #print(event.x, event.y)
        color = self.colors[self.t%2]
        if not(self.itemClicked)  ==  False:
            for r in range(len(self.board.grid)):
                for c in range(len(self.board.grid[r])):
                    lH = 10 + 96*r
                    lW = 10 + 96*c
                    if event.x in range(lW, lW+90) and event.y in range(lH, lH+90) and self.board.grid[r][c] !=  0 and \
                        self.board.pieces[self.board.grid[r][c]][1]  ==  color:
                        self.canvas.create_image(
                        	lW, lH, image = self.emptySpaces[3], anchor = NW
                        )
                        self.canvas.create_image(
                        	lW, lH, image = self.pieces[self.board.grid[r][c]], anchor = NW
                        )
                        self.itemClicked = False
                        self.curPos = [r, c]
        else:
            for r in range(len(self.board.grid)):
                for c in range(len(self.board.grid[r])):
                    lH = 10 + 96*r
                    lW = 10 + 96*c
                    if event.x in range(lW, lW+90) and event.y in range(lH, lH+90):
                        if r  ==  self.curPos[0] and c  ==  self.curPos[1]:
                            self.canvas.create_image(
                            	lW, lH, image = self.emptySpaces[(r+c)%2], anchor = NW
                            )
                            self.canvas.create_image(
                            	lW, lH, image = self.pieces[self.board.grid[r][c]], anchor = NW, activeimage = self.activePieces[self.board.grid[r][c]]
                            )
                            self.itemClicked = True
                        else:
                            self.finPos = [r, c]
                            if self.board.turnValid(self.board.grid, self.curPos, self.finPos, color):
                                self.itemClicked = True
                                self.t +=  1
                                #Add to missing pieces list ---------------------------------------------------
                                if self.board.grid[self.finPos[0]][self.finPos[1]]%6 > 1 and color  ==  'White':
                                    self.missingPiecesBlack.append(self.board.grid[self.finPos[0]][self.finPos[1]])
                                    if len(self.missingPiecesBlack) > 4:
                                        self.missingPiecesBlack.remove(min(self.missingPiecesBlack))
                                elif self.board.grid[self.finPos[0]][self.finPos[1]]%6 > 1 and color  ==  'Black':
                                    self.missingPiecesWhite.append(self.board.grid[self.finPos[0]][self.finPos[1]])
                                    if len(self.missingPiecesWhite) > 4:
                                        self.missingPiecesWhite.remove(min(self.missingPiecesWhite))
                                # --------------------------------------------------------------
                                self.board.grid[self.finPos[0]][self.finPos[1]] = self.board.grid[self.curPos[0]][self.curPos[1]]
                                self.board.grid[self.curPos[0]][self.curPos[1]] = 0
                                #Pawn promotion -----------------------------------------------------------
                                if (self.board.grid[self.finPos[0]][self.finPos[1]]  ==  1 and r  ==  7) or \
                                   (self.board.grid[self.finPos[0]][self.finPos[1]]  ==  7 and r  ==  0):
                                    if color  == 'White' and len(self.missingPiecesWhite) > 0:
                                        self.board.grid[self.finPos[0]][self.finPos[1]] = max(self.missingPiecesWhite)
                                        self.missingPiecesWhite.remove(max(self.missingPiecesWhite))
                                    elif color  ==  "Black" and len(self.missingPiecesBlack) > 0:
                                        self.board.grid[self.finPos[0]][self.finPos[1]] = max(self.missingPiecesBlack)
                                        self.missingPiecesBlack.remove(max(self.missingPiecesBlack))
                                # -----------------------------------------------------------
                                self.canvas.delete(ALL)
                                self.displayBoard()

                            if self.comOp  ==  True and self.t%2  ==  1:
                                color = self.colors[self.t%2]
                                choice = self.computer.makeMove(self.board, color)
                                #Add to missing pieces list ---------------------------------------------------
                                if self.board.grid[choice[2][0]][choice[2][1]]%6 > 1 and color  ==  'Black':
                                    self.missingPiecesWhite.append(self.board.grid[choice[2][0]][choice[2][1]])
                                    if len(self.missingPiecesWhite) > 4:
                                        self.missingPiecesWhite.remove(min(self.missingPiecesWhite))
                                elif self.board.grid[choice[2][0]][choice[2][1]]%6 > 1 and color  ==  'White':
                                    self.missingPiecesBlack.append(self.board.grid[choice[2][0]][choice[2][1]])
                                    if len(self.missingPiecesBlack) > 4:
                                        self.missingPiecesBlack.remove(min(self.missingPiecesBlack))
                                # -----------------------------------------------------------
                                self.board.grid[choice[2][0]][choice[2][1]] = self.board.grid[choice[1][0]][choice[1][1]]
                                self.board.grid[choice[1][0]][choice[1][1]] = 0
                                #Pawn promotion -----------------------------------------------------------
                                if (self.board.grid[choice[2][0]][choice[2][1]]  ==  1 and r  ==  7) or \
                                   (self.board.grid[choice[2][0]][choice[2][1]]  ==  7 and r  ==  0):
                                    if color  ==  'Black' and len(self.missingPiecesBlack) > 0:
                                        self.board.grid[choice[2][0]][choice[2][1]] = max(self.missingPiecesBlack)
                                        self.missingPiecesBlack.remove(max(self.missingPiecesBlack))
                                    elif color  ==  "White" and len(self.missingPiecesWhite) > 0:
                                        self.board.grid[choice[2][0]][choice[2][1]] = max(self.missingPiecesWhite)
                                        self.missingPiecesWhite.remove(max(self.missingPiecesWhite))
                                # -----------------------------------------------------------
                                print("From " + str(choice[1]) + " To " + str(choice[2]))
                                self.t +=  1
                                self.canvas.delete(ALL)
                                self.displayBoard()
        self.Master.update()
	

    def Computer(self):
        color = self.colors[self.t%2]
        for r in range(len(self.board.grid)):
            for c in range(len(self.board.grid[r])):
                color = self.colors[self.t%2]
                choice = self.computer.makeMove(self.board, color)
                #Add to missing pieces list ---------------------------------------------------
                if self.board.grid[choice[2][0]][choice[2][1]]%6 > 1 and color  ==  'Black':
                    self.missingPiecesWhite.append(self.board.grid[choice[2][0]][choice[2][1]])
                    if len(self.missingPiecesWhite) > 4:
                        self.missingPiecesWhite.remove(min(self.missingPiecesWhite))
                elif self.board.grid[choice[2][0]][choice[2][1]]%6 > 1 and color  ==  'White':
                    self.missingPiecesBlack.append(self.board.grid[choice[2][0]][choice[2][1]])
                    if len(self.missingPiecesBlack) > 4:
                        self.missingPiecesBlack.remove(min(self.missingPiecesBlack))
                # -----------------------------------------------------------
                self.board.grid[choice[2][0]][choice[2][1]] = self.board.grid[choice[1][0]][choice[1][1]]
                self.board.grid[choice[1][0]][choice[1][1]] = 0

                #Pawn promotion -----------------------------------------------------------
                if (self.board.grid[choice[2][0]][choice[2][1]]  ==  1 and r  ==  7) or \
                   (self.board.grid[choice[2][0]][choice[2][1]]  ==  7 and r  ==  0):
                    if color  ==  'Black' and len(self.missingPiecesBlack) > 0:
                        self.board.grid[choice[2][0]][choice[2][1]] = max(self.missingPiecesBlack)
                        self.missingPiecesBlack.remove(max(self.missingPiecesBlack))
                    elif color  ==  "White" and len(self.missingPiecesWhite) > 0:
                        self.board.grid[choice[2][0]][choice[2][1]] = max(self.missingPiecesWhite)
                        self.missingPiecesWhite.remove(max(self.missingPiecesWhite))
                # -----------------------------------------------------------
                print("From " + str(choice[1]) + " To " + str(choice[2]))
                self.t +=  1
                if self.isStopped:
                    self.displayBoard()
                else:
                    exit()



if __name__ ==  "__main__":
    print("\n======= New Game =======")

    root = tk.Tk()
    app = App(root, sys.argv[1])
    if sys.argv[1]  ==  'AI_AI':
        app.Computer()
        
    elif sys.argv[1] == 'Human_Human' or sys.argv[1] == 'AI_Human':
    	app.canvas.bind("<Button-1>", app.callback)
    else:
        print('Argument Error...')
        exit()
    
    root.mainloop()