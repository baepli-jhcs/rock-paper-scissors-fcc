# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import pandas as pd
import numpy as np

# This one works
n = 3
STATES = ["R", "P", "S"]

labels = []
for first in STATES:
    for second in STATES:
        for third in STATES:
            for fourth in STATES:
                labels.append(first + second + third + fourth)

table = pd.Series(np.zeros(3 ** (n + 1)), index=labels)


def player(prev_play, opponent_history=[]):

    if prev_play == "":
        reset()
        return "S"

    opponent_history.append(prev_play)

    if len(opponent_history) <= n:
        return "R"

    history = "".join(opponent_history[-n - 1 :])

    table[history] += 1

    solutions = [history[1:] + "R", history[1:] + "P", history[1:] + "S"]

    prediction = find_max(solutions)

    if prediction[-1] == "R":
        return "P"
    elif prediction[-1] == "P":
        return "S"
    return "R"


def find_max(solutions):
    max = 0
    label = ""
    for solution in solutions:
        if table[solution] >= max:
            label = solution
            max = table[solution]

    return label


def reset():
    global table
    table = pd.Series(np.zeros(3 ** (n + 1)), index=labels)
