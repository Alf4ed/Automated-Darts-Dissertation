# import tkinter module
from tkinter import *
from tkinter.ttk import *
from tkinter.font import BOLD
import random, math

# Creat tkinter window
root = Tk()

# Set background color
root.configure(background='#282C34')

playerA = Canvas(root, background = 'grey', highlightthickness = 0)
playerA.grid(row = 0, column = 0, sticky = W, padx = (25,0), pady = (20,0))

playerB = Canvas(root, background = 'grey', highlightthickness = 0)
playerB.grid(row = 1, column = 0, sticky = W, padx = (25,0), pady = (20,0))

edit = Canvas(root, background = '#282C34', highlightthickness = 0)
edit.grid(row = 2, column = 0, sticky = W, padx = (25,0), pady = 20)

boardA = Canvas(root, background = '#282C34', highlightthickness = 0)
boardA.grid(row = 0, column = 1, sticky = W, padx = 20, pady = 20, rowspan = 3)
boardB = Canvas(root, background = '#282C34', highlightthickness = 0)
boardB.grid(row = 0, column = 2, sticky = W, padx = 20, pady = 20, rowspan = 3)

nameA = Label(playerA, text = "Alfred", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
nameA.grid(row = 0, column = 0, sticky = W, pady = 2, padx = 50, columnspan = 2)
scoreA = Label(playerA, text = "423", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
scoreA.grid(row = 0, column = 2, sticky = E, pady = 2, padx = 50)

aDart1 = Label(playerA, text = "22", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
aDart1.grid(row = 1, column = 0, sticky = W, pady = 2, padx = 50)
aDart2 = Label(playerA, text = "35", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
aDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
aDart3 = Label(playerA, text = "77", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
aDart3.grid(row = 1, column = 2, sticky = E, pady = 2, padx = 50)

nameB = Label(playerB, text = "Alan", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
nameB.grid(row = 0, column = 0, sticky = W, pady = 2, padx = 50, columnspan = 2)
scoreB = Label(playerB, text = "94", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
scoreB.grid(row = 0, column = 2, sticky = E, pady = 2, padx = 50)

bDart1 = Label(playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
bDart1.grid(row = 1, column = 0, sticky = W, pady = 2, padx = 50)
bDart2 = Label(playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
bDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
bDart3 = Label(playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
bDart3.grid(row = 1, column = 2, sticky = E, pady = 2, padx = 50)

undo = Button(edit, text = 'Undo', width = 10)
undo.grid(row = 0, column = 0, sticky = W, pady = 5)
override = Entry(edit, width = 11)
override.grid(row = 1, column = 0, sticky = W, pady = 5)
instructions = Button(edit, text = 'Enter', width = 5)
instructions.grid(row = 1, column = 1, sticky = W, pady = 5, padx = 5)

img = PhotoImage(file = r"result.png")
img1 = img.subsample(3, 3)
Label(boardA, image = img1, background='#282C34').grid(row = 0, column = 0, padx = 20, pady = 20)
Label(boardB, image = img1, background='#282C34').grid(row = 0, column = 0, padx = 20, pady = 20)

def update():
    score = random.random()
    score = math.floor(score*61)
    bDart1.config(text = str(score))
    root.after(1000, update)

update()
mainloop()