import tkinter as tk
from tkinter.ttk import *
from tkinter.font import BOLD
from thread import override

class GUI():
    def __init__(self):
        # Creat tkinter window
        self.root = tk.Tk()

        # Set background color
        self.root.configure(background='#282C34')

    def createLayout(self):
        self.playerA = tk.Canvas(self.root, background = 'grey', highlightthickness = 0)
        self.playerA.grid(row = 0, column = 0, sticky = tk.W, padx = (25,0), pady = (20,0))

        self.playerB = tk.Canvas(self.root, background = 'grey', highlightthickness = 0)
        self.playerB.grid(row = 1, column = 0, sticky = tk.W, padx = (25,0), pady = (20,0))

        self.edit = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.edit.grid(row = 2, column = 0, sticky = tk.W, padx = (25,0), pady = 20)

        self.undo = tk.Button(self.edit, text = 'Undo', width = 5, background = 'grey', font = ('Arial', 12, BOLD), foreground = '#CCCCCC')
        self.undo.grid(row = 0, column = 0, sticky = tk.W, pady = 5)
        self.override = tk.Entry(self.edit, width = 5, font = ('Arial', 12, BOLD))
        self.override.grid(row = 1, column = 0, sticky = tk.W, pady = 5)
        self.instructions = tk.Button(self.edit, text = 'Enter', command = self.manual, width = 5, background = 'grey', font = ('Arial', 12, BOLD), foreground = '#CCCCCC')
        self.instructions.grid(row = 1, column = 1, sticky = tk.W, pady = 5, padx = 5)

        self.boardA = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.boardA.grid(row = 0, column = 1, sticky = tk.W, pady = 20, rowspan = 3)
        self.boardB = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.boardB.grid(row = 0, column = 2, sticky = tk.W, pady = 20, rowspan = 3)

    def createPlayers(self, playerOneName, playerTwoName):
        self.nameA = tk.Label(self.playerA, text = playerOneName, background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
        self.nameA.grid(row = 0, column = 0, sticky = tk.W, pady = 2, padx = 50, columnspan = 2)
        self.scoreA = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
        self.scoreA.grid(row = 0, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.aDart1 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart1.grid(row = 1, column = 0, sticky = tk.W, pady = 2, padx = 50)
        self.aDart2 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
        self.aDart3 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart3.grid(row = 1, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.nameB = tk.Label(self.playerB, text = playerTwoName, background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
        self.nameB.grid(row = 0, column = 0, sticky = tk.W, pady = 2, padx = 50, columnspan = 2)
        self.scoreB = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
        self.scoreB.grid(row = 0, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.bDart1 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart1.grid(row = 1, column = 0, sticky = tk.W, pady = 2, padx = 50)
        self.bDart2 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
        self.bDart3 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart3.grid(row = 1, column = 2, sticky = tk.E, pady = 2, padx = 50)

    def setBoardImage(self, img):
        tk.Label(self.boardA, image = img, background='#282C34').grid(row = 0, column = 0, pady = 20)

    def setOptimalImage(self, img):    
        tk.Label(self.boardB, image = img, background='#282C34').grid(row = 0, column = 0, pady = 20)

    def start(self):
        tk.mainloop()

    def manual(self):
        override(self.override.get())
        self.override.delete(0, 'end')