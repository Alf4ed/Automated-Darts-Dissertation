import numpy as np
import normal
import matplotlib.pyplot as plt
import math

skill = normal.Normal()

std = [i for i in range(1, 101)]
expected_scores = []
expected_scores20 = []
percentageIncrease = []
checkout501 = []
checkout50120 = []

for i in range(1, 101):
    x, y = skill.create_kernel(401, std=i)
    es = skill.calculate_expected_score(x, y)
    expected_scores.append(es.max())
    expected_scores20.append(es[96][200])

for i, score in enumerate(expected_scores):
    percentageIncrease.append(100*(expected_scores[i]-expected_scores20[i])/expected_scores20[i])

for i, score in enumerate(expected_scores):
    checkout501.append(math.ceil(461/expected_scores[i]/3))
    checkout50120.append(math.ceil(461/expected_scores20[i]/3))

# plt.plot(std, checkout501, color='#267F54', label='Aiming at Optimal Location')  # Plot the chart
# plt.plot(std, checkout50120, color='#E3292E', label='Aiming at T20')
plt.plot(std, percentageIncrease, color='#1E90FF')
plt.title('Increase in Expected Score vs. Player Skill')
plt.xlabel('Standard Deviation (mm)')
plt.ylabel('Increase in Expected Score (%)')
# plt.legend(loc="lower right")
plt.savefig('es.png', bbox_inches='tight', pad_inches=0, dpi=700, transparent=True)
plt.show()  # display