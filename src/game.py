class Player():
    def __init__(self, name, game):
        self.name = name
        self.history = []
        self.score = game
        self.turn = 0
        self.display = ['-','-','-']
    
    def dart(self, value, double):
        if self.score - value == 0 and double == True:
            print('Player', self.name, 'wins!')
            exit()
        if self.score - value >= 2:
            self.score = self.score - value
            self.history.append(value)
            self.display[self.turn] = (value)
            self.turn = (self.turn + 1) % 3
        else:
            self.display[self.turn] = ('X')
            self.history.append('N/A')
            self.turn = 0
    
    def undo(self):
        self.score += self.history.pop()
        self.turn = (self.turn - 1) % 3
        self.display[self.turn] = '-'
        
class dartGame():
    def __init__(self, playerAName, playerBName, game=501):
        self.game = game
        self.players = (Player(playerAName, game), Player(playerBName, game))
        self.activePlayer = 0
        self.justChanged = True
        self.change = True
        self.inBoard = []

    def dart(self, value, double):
        self.justChanged = False
        self.players[self.activePlayer].dart(value, double)
        self.change = True

    def changeOver(self):
        if self.justChanged == False:
            self.activePlayer = (self.activePlayer + 1) % 2
            self.change = True
            self.justChanged = True
            self.players[self.activePlayer].display = ['-','-','-']
            self.players[self.activePlayer].turn = 0

    def undo(self):
        if self.players[self.activePlayer].turn > 0:
            self.players[self.activePlayer].undo()
        else:
            self.changeOver()
            self.undo()
        
        self.change = True