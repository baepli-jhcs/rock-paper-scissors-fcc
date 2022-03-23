# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import pandas as pd
import numpy as np
import random

# Q-tables do not work, this gets ~55% for Abbey
n=2
STATES = ["R", "P", "S"]
table = pd.DataFrame(np.zeros((3**n, 3)), columns=["R", "P", "S"])

LEARNING_RATE = 1.0
GAMMA = 0.92
epsilon = 0.9

last_action="P"

labels = []
for outer in STATES:
  for inner in STATES:
      labels.append(outer + inner)

table.index = labels

combinations = {
  "R": {
    "R": 0,
    "P": 1,
    "S": -1
  },
  "P": {
    "R": -1,
    "P": 0,
    "S": 1
  },
  "S": {
    "R": 1,
    "P": -1,
    "S": 0
  }
}

def player(prev_play, opponent_history=[]):
  global table, last_action, epsilon

  if prev_play == "":
    reset_values()
    return "P"
    
  opponent_history.append(prev_play)
  
  if len(opponent_history) <= n:
    return "P"
    
  reward = combinations[prev_play][last_action]

  last_state = "".join(opponent_history[-1-n: -1])
  new_state = "".join(opponent_history[-n:])
  table.loc[last_state, last_action] += LEARNING_RATE * (reward + GAMMA * table.loc[new_state].max() - table.loc[last_state, last_action])
  if np.random.uniform(0, 1) < epsilon:
    random_choice = random.choice(STATES)
    last_action = random_choice
  else:
    last_action = table.idxmax(axis="columns").loc[new_state]
  epsilon-=0.0017
  return last_action

def reset_values():
  global table, epsilon
  table = pd.DataFrame(np.zeros((3**n, 3)), columns=["R", "P", "S"], index=labels)
  epsilon = 0.6