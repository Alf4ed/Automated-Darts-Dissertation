from enum import Enum

class CameraMode(Enum):
    OFF = 'OFF'
    ON = 'ON'
    POSITIONING = 'POSITIONING'
    GAME = 'GAME'

class Admin:
    def __init__(self):
        self.mode = CameraMode.OFF
        self.frames = [None, None, None]
        self.aimbot = None
        self.center_line = False
        self.skills = []

class Dart:
    STRING_REP = ('', 'S', 'D', 'T')

    def __init__(self, score, multiplier, position):
        self.score = int(score)
        self.multiplier = int(multiplier)
        self.position = position

    def value(self):
        return self.score * self.multiplier
    
    def is_double(self):
        return self.multiplier == 2

    def to_string(self):
        return self.STRING_REP[self.multiplier] + str(self.score)
    
    def is_bust(self):
        return False
    
    def get_position(self):
        return self.position

class Bust(Dart):
    def __init__(self, dart):
        super().__init__(dart.score, dart.multiplier, dart.position)

    def is_bust(self):
        return True
    
    def value(self):
        return 0
    
    def to_string(self):
        return 'BUST'
    
class Turn:
    def __init__(self, player):
        self.darts = []
        self.player = player
    
    def dart(self, dart):
        self.darts.append(dart)

    def bust(self, dart):
        for i in self.darts:
            self.player.undo_dart(i)
        self.darts.append(Bust(dart))

    def display(self):
        representation = ['-', '-', '-']

        for i in range(min(3, len(self.darts))):
            representation[i] = self.darts[i].to_string()
        
        return representation
    
    def is_over(self):
        if len(self.darts) == 0:
            return False
        
        return len(self.darts) >= 3 or self.darts[-1].is_bust()

class Leg:
    def __init__(self, players, current_player):
        self.current_turn = Turn(players[current_player])
        self.turns = [self.current_turn]
        self.winner = None
        self.players = players
        self.current_player = self.players[current_player]
        self.player_index = current_player
        self.change = False
    
    def dart(self, dart):
        if not self.current_player.is_bust(dart):
            self.current_turn.dart(dart)
            self.current_player.dart(dart)
        else:
            self.current_turn.bust(dart)

        if self.current_turn.is_over():
            self.changeover()

    def get_last_turn(self, player):
        for turn in reversed(self.turns):
            if turn.player == player:
                return turn.display()
        
        return ['-', '-', '-']

    def changeover(self):
        self.player_index = (self.player_index + 1) % 2
        self.current_player = self.players[(self.player_index)]
        self.current_turn = Turn(self.current_player)
        self.turns.append(self.current_turn)
        self.change = True

class Player:
    def __init__(self, name, format):
        self.name = name
        self.format = format
        self.score = format
        self.wins = 0

    def dart(self, dart):
        self.score -= dart.value()

    def undo_dart(self, dart):
        self.score += dart.value()
        
    def is_bust(self, dart):
        result = self.score - dart.value()

        if result == 1 or result < 0:
            return True
        if result == 0 and not dart.is_double:
            return True
        
        return False
    
    def has_won(self):
        return self.score == 0

    def reset(self):
        self.score = self.format

# Game class stores information about the current game being played between two players
# The Front-end and Back-end use a shared Game class object to interface
class Game:
    def __init__(self):
        self.positions = []
        self.new_positions = []
        self.playing = False
        self.update = False

    def start_game(self, first_to, format, name_a, name_b):
        self.first_to = first_to
        self.legs_played = []
        self.format = format
        self.players = (Player(name_a, format), Player(name_b, format))
        self.current_leg = Leg(self.players, len(self.legs_played) % 2)
        self.playing = True
        self.update = True
        self.clear = False
        self.just_won = False

    def dart(self, dart):
        self.current_leg.dart(dart)
        self.has_won()
        self.update = True

    def has_won(self):
        for player in self.players:
            if player.has_won():
                self.current_leg.winner = player
                player.wins += 1
                self.reset()
                self.legs_played.append(self.current_leg)
                self.current_leg = Leg(self.players, len(self.legs_played) % 2)
                self.just_won = True
    
    def get_scores(self):
        if self.playing == True:
            return [self.current_leg.get_last_turn(self.players[0]), self.current_leg.get_last_turn(self.players[1])]
        else:
            return -1
        
    def get_wins(self):
        if self.playing == True:
            return [self.players[0].wins, self.players[1].wins]
        else:
            return -1
    
    def get_totals(self):
        if self.playing:
            return [self.players[0].score, self.players[1].score]
        else:
            return -1
    
    def new_dart(self, dart):
        self.positions.append(dart)
        self.new_positions.append(dart)

    def get_positions(self):
        return [x.get_position() for x in self.positions]

    def get_new_dart(self):
        if not self.new_positions:
            return None, '-'
        
        dart = self.new_positions.pop()
        position = dart.get_position()
        score = dart.to_string()

        return position, score
    
    def change(self):
        result =  self.current_leg.change
        self.current_leg.change = False
        return result
    
    def has_just_won(self):
        result = self.just_won
        self.just_won = False
        return result, self.current_leg.player_index
    
    def is_clear(self):
        result = self.clear
        self.clear = False
        return result
    
    def clear_board(self):
        self.clear = True
    
    def is_updated(self):
        result = self.update
        self.update = False
        return result
    
    def reset(self):
        for player in self.players:
            player.reset()