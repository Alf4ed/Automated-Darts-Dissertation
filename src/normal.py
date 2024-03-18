import numpy as np
from scipy import signal
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle
import math
import display
import gameData
import time
import io

# All double totals on the board
DOUBLES = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,50]

# Impossible scores to hit in n darts
IMPOSSIBLE_SCORES = [[23,29,31,35,37,41,43,44,46,47,49,52,53,55,56,58,59],  # 1 dart
                    [103,106,109,112,113,115,116,118,119],                  # 2 darts
                    [163,166,169,172,173,175,176,178,179],                  # 3 darts
                    [223,226,229,232,233,235,236,238,239],                  # 4 darts
                    [283,286,289,292,293,295,296,298,299],                  # 5 darts
                    [343,346,349,352,353,355,356,358,359]]                  # 6 darts

# Impossible scores to checkout in n darts (the final dart must be a DOUBLE)
IMPOSSIBLE_CHECKOUTS = [[0,1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,59,60],    # 1 dart
                        [0,1,99,102,103,105,106,108,109,111,112,113,114,115,116,117,118,119,120],                                               # 2 darts
                        [0,1,159,162,163,165,166,168,169,171,172,173,174,175,176,177,178,179,180]]                                              # 3 darts

class Normal():
    def __init__(self):
        # Store probabilities for all aim locations
        self.DOUBLE_REGION_PROBABILITIES = dict()
        self.SCORING_REGION_PROBABILITIES = dict()

        # Store the maximum checkout probability for each total
        self.CHECKOUT_PROBABILITIES = [dict(), dict(), dict(), dict(), dict()]

        self.EXPECTED_SCORE = None

    # Calculate the 2D skill kernel
    def create_kernel(self, size, data_x=None, data_y=None, std=20):
        x, y = [], []

        # Use a players dart locations from skill calculation if they exist
        # Otherwise model as a standard circular normal distribution with standard deviation of 20mm
        if data_x is None or data_y is None:
            ax, locx, scalex = 0, 0, std
            ay, locy, scaley = 0, 0, std
        else:
            ax, locx, scalex = skewnorm.fit(data_x)
            ay, locy, scaley = skewnorm.fit(data_y)

        skewnorm_dist_x = skewnorm(ax, locx, scalex)
        skewnorm_dist_y = skewnorm(ay, locy, scaley)

        # Use cdf to bin the data
        for i in range(-math.floor(size/2), math.ceil(size/2)):
            leftx = skewnorm_dist_x.cdf(i-0.5)
            rightx = skewnorm_dist_x.cdf(i+0.5)
            x.append(rightx-leftx)

            lefty = skewnorm_dist_y.cdf(i-0.5)
            righty = skewnorm_dist_y.cdf(i+0.5)
            y.append(righty-lefty)

        # Return the horizontal and vertical discrete distributions
        return x, y
    
    # For all aim locations on the board, calculate the expected value given the players skill
    def calculate_expected_score(self, horizontal, vertical):
        totals = np.fromfunction(np.vectorize(lambda i, j: display.score_dart(j-200, 200-i).value()), (400, 400))
        
        horizontal = np.array(horizontal)
        horizontal = horizontal.reshape(1, -1)
        vertical = np.array(vertical)
        vertical = vertical.reshape(1, -1)

        # Perform two 1D convolutions as this is faster than one 2D convolution
        resultA = signal.correlate(totals, horizontal, mode='same')
        probabilities = signal.correlate(resultA, vertical.T, mode='same')
        
        return probabilities

    # For all aim locations on the board, and a given total, calculate the probability of hitting this total
    def calculate_region_probability(self, total, horizontal, vertical, checkout):
        scores = np.fromfunction(np.vectorize(lambda i, j: display.score_prob(i-200, j-200, total, checkout)), (400, 400))

        horizontal = np.array(horizontal)
        horizontal = horizontal.reshape(1, -1)
        vertical = np.array(vertical)
        vertical = vertical.reshape(1, -1)

        # Perform two 1D convolutions as this is faster than one 2D convolution
        resultA = signal.correlate(scores, horizontal, mode='same')
        probabilities = signal.correlate(resultA, vertical.T, mode='same')
        
        return probabilities

    # For all aim locations on the board, and for all possible one dart scores, calculate the probability of hitting this score
    def calculate_region_probabilities(self, horizontal, vertical):
        # Calculate probabilities for doubles
        for total in DOUBLES:
            self.DOUBLE_REGION_PROBABILITIES[total] = self.calculate_region_probability(total, horizontal, vertical, True)
        
        # Calculate probabilities for all totals
        for total in range(0,61):
            if total in IMPOSSIBLE_SCORES[0]:
                continue

            self.SCORING_REGION_PROBABILITIES[total] = self.calculate_region_probability(total, horizontal, vertical, False)
        
    def calculate_n_dart_checkout_probabilities(self, n_darts):
        for total in range(0, 60*n_darts):
            if total in IMPOSSIBLE_SCORES[n_darts-1]:
                continue

            if total not in self.DOUBLE_REGION_PROBABILITIES:
                a = 0
            else:
                a = self.DOUBLE_REGION_PROBABILITIES[total]
            
            probabilities = a

            for region in range(0, 61):
                if region in IMPOSSIBLE_SCORES[0]:
                    continue

                if (total-region) in self.CHECKOUT_PROBABILITIES[n_darts-2]:
                    b = np.multiply(self.CHECKOUT_PROBABILITIES[n_darts-2][total-region], self.SCORING_REGION_PROBABILITIES[region])
                else:
                    b = 0
                
                probabilities = np.add(probabilities, b)

            self.CHECKOUT_PROBABILITIES[n_darts-1][total] = probabilities.max()

    def calculate_checkout_probabilities(self):
        for total in DOUBLES:
            self.CHECKOUT_PROBABILITIES[0][total] = self.DOUBLE_REGION_PROBABILITIES[total].max()

        for n_darts in range(1, 6):
            self.calculate_n_dart_checkout_probabilities(n_darts)

    def optimal_n_darts(self, total, n):

        if total in IMPOSSIBLE_CHECKOUTS[n-1] or total > n*60:
            n += 3

        if total < 0 or n*60 < total or total > 180:
            return self.EXPECTED_SCORE
        elif total in IMPOSSIBLE_SCORES[n-1]:
            return self.EXPECTED_SCORE

        if n == 1:
            return self.DOUBLE_REGION_PROBABILITIES[total]
        
        if total not in self.DOUBLE_REGION_PROBABILITIES:
            a = 0
        else:
            a = self.DOUBLE_REGION_PROBABILITIES[total]

        probabilities = a

        for region in range(0, 61):
            if region in IMPOSSIBLE_SCORES[0]:
                continue

            if (total-region) in self.CHECKOUT_PROBABILITIES[n-2]:
                b = np.multiply(self.CHECKOUT_PROBABILITIES[n-2][total-region], self.SCORING_REGION_PROBABILITIES[region])
            else:
                b = 0

            probabilities = np.add(probabilities, b)

        return probabilities
    
def add_text(color='gray'):
    sectors = ['10','15','2','17','3','19','7','16','8','11','14','9','12','5','20','1','18','4','13','6']

    for i in range(0, 20):
        x = math.cos((18/180)*math.pi + 2*math.pi/20*i)*200
        y = math.sin((18/180)*math.pi + 2*math.pi/20*i)*200

        plt.text(x+200, y+200, sectors[i], horizontalalignment='center',
                    verticalalignment='center', fontsize=12, color=color)

def draw_radius(color='gray'):
    for i in range(0, 20):
        x1 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*16+200
        y1 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*16+200

        x2 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*170+200
        y2 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*170+200
    
        x1, y1 = [x1, x2], [y1, y2]
        plt.plot(x1, y1, color=color, linewidth=1)

    circle1 = Circle((200, 200), radius=170, color=color, fill=False, linewidth=1)
    circle2 = Circle((200, 200), radius=162, color=color, fill=False, linewidth=1)
    circle3 = Circle((200, 200), radius=107, color=color, fill=False, linewidth=1)
    circle4 = Circle((200, 200), radius=99, color=color, fill=False, linewidth=1)
    circle5 = Circle((200, 200), radius=16, color=color, fill=False, linewidth=1)
    circle6 = Circle((200, 200), radius=6.35, color=color, fill=False, linewidth=1)
        
    plt.gca().add_patch(circle1)
    plt.gca().add_patch(circle2)
    plt.gca().add_patch(circle3)
    plt.gca().add_patch(circle4)
    plt.gca().add_patch(circle5)
    plt.gca().add_patch(circle6)

newcmp = cm.get_cmap('viridis')
newcmp.set_bad('#267F54')
newcmp.set_bad('#FFFFFF00')

def get_players_skill(admin, lock, player):
    result = None

    lock.acquire()
    for element in admin.skills:
        if element[0] == player:
            result = element[1]
            break
    lock.release()

    return np.array(result) if result is not None else None

def start_normal(admin, game, lock):

    players = []

    for i in range(0, 2):
        a = Normal()
        ax, ay = a.create_kernel(201, std=(10*(1+i)))
        a.calculate_region_probabilities(ax, ay)
        a.calculate_checkout_probabilities()
        a.EXPECTED_SCORE = a.calculate_expected_score(ax, ay)
        players.append(a)
    
    print("READY")

    while True:
        lock.acquire()

        if admin.mode == gameData.CameraMode.GAME and game.is_updated():
            player = players[game.current_leg.player_index]
            plt.clf()
            prob = player.optimal_n_darts(game.current_leg.current_player.score, 3-len(game.current_leg.current_turn.darts))
            
            # Create a grid of x, y coordinates
            x, y = np.meshgrid(np.arange(400), np.arange(400))

            # Calculate distance from center for each point
            distance_from_center = np.sqrt((x - 200)**2 + (y - 200)**2)

            # Create a mask for values outside of the circle with radius 180
            mask = distance_from_center > 180
            prob[mask] = np.nan

            plt.imshow(prob, cmap=newcmp)
            buf = io.BytesIO()

            max_index = np.unravel_index(np.nanargmax(prob), prob.shape)
            # Plot a point at the location of the max value
            plt.scatter(max_index[1], max_index[0], color='#E3292E', marker='x')

            add_text(color='#282C34')
            draw_radius(color='#282C3455')
            
            plt.axis('off')
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=350, transparent=True)
            admin.aimbot = buf
            buf.seek(0)
        
        lock.release()

        time.sleep(0.5)

if __name__ == "__main__":
    skill = Normal()
    x, y = skill.create_kernel(401)
    # skill.calculate_region_probabilities(x, y)
    # skill.calculate_checkout_probabilities()
    # result = skill.optimal_n_darts(47, 6)
    result = np.fromfunction(np.vectorize(lambda i, j: display.score_prob(i-200, j-200, 6, False)), (400, 400))
    
    # kernel = np.outer(x, y)
    # totals = np.fromfunction(np.vectorize(lambda i, j: display.score_dart(j-200, 200-i).value()), (400, 400))
    # expected = skill.calculate_expected_score(x, y)

    # x = np.array(x)
    # x = x.reshape(1, -1)

    x, y = np.meshgrid(np.arange(400), np.arange(400))

    # Calculate distance from center for each point
    distance_from_center = np.sqrt((x - 200)**2 + (y - 200)**2)
    
    mask = distance_from_center > 180
    # result[mask] = np.nan

    result_masked = np.ma.array(result, mask=mask)

    # Replace masked elements with NaN
    result_masked = np.where(mask, np.nan, result_masked)

    plt.imshow(result_masked, cmap=newcmp)
    # max_index = np.unravel_index(np.nanargmax(result), result.shape)
    # Plot a point at the location of the max value
    # plt.scatter(max_index[1], max_index[0], color='#E3292E', marker='x')
    add_text(color='#282C34')
    draw_radius(color='#282C3455')
    
    plt.axis('off')
    # plt.colorbar()
    plt.savefig("47", bbox_inches='tight', pad_inches=0, dpi=700, transparent=True)



