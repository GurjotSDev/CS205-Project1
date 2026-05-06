import time
import sys

# This is to allow for simple changes to the puzzle, just make sure its valid
trench_Len = 10
recess_Pos = (3, 5, 7)
num_Recess = 3

# The current state of the problem
initial_Trench = (0, 2, 3, 4, 5, 6, 7, 8, 9, 1)
initial_Recess = (0, 0, 0)

# The goal state
goal_Trench = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
goal_Recess = (0, 0, 0)

