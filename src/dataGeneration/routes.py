import numpy as np
import normal
import display

skill = normal.Normal()
x, y = skill.create_kernel(401)

skill.calculate_region_probabilities(x, y)
skill.calculate_checkout_probabilities()

for i in range(2, 180):
    out1, out2, out3 = "", "", ""
    if i not in normal.IMPOSSIBLE_CHECKOUTS[2]:
        result = skill.optimal_n_darts(i, 3)
        max_index = np.unravel_index(np.nanargmax(result), result.shape)

        aim = display.score_dart(max_index[1]-200, 200-max_index[0])
        out1 = aim.to_string()

        if i-aim.value() == 0:
            pass
        elif i-aim.value() not in normal.IMPOSSIBLE_CHECKOUTS[1]:
            result2 = skill.optimal_n_darts(i - aim.value(), 2)
            max_index2 = np.unravel_index(np.nanargmax(result2), result2.shape)
            aim2 = display.score_dart(max_index2[1]-200, 200-max_index2[0])
            out2 = aim2.to_string()

            if i-aim.value()-aim2.value() == 0:
                pass
            elif i-aim.value()-aim2.value() not in normal.IMPOSSIBLE_CHECKOUTS[0]:
                result3 = skill.optimal_n_darts(i - aim.value() - aim2.value(), 1)
                max_index3 = np.unravel_index(np.nanargmax(result3), result3.shape)
                aim3 = display.score_dart(max_index3[1]-200, 200-max_index3[0])
                out3 = aim3.to_string()
            else:
                out3 = "IMPOSSIBLE"
        else:
            out2 = "IMPOSSIBLE"
    else:
        out1 = "IMPOSSIBLE"

    print("Total:",i,"Aim:",out1, out2, out3)