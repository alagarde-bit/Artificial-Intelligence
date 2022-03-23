#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
"""Assignment 4 (8 Queens game) """
_author_ = "Alex Lagarde"
# importing libraries 
import random
import sys
import math

# 8 queens heuristic function
def heuristic(queen_positions):
    board = queen_positions
    h = 0
    # looping i from 0 to 7
    for i in range(len(board)):
    # looping j from i+1, 7
        for j in range(i+1,len(board)):
            # calculating the absolute values of column and row differences for diagonal check
            col_diff = abs(j-i)
            row_diff = abs(board[i] - board[j])
            # checking same row
            if board[i] == board[j]:
                h+=1
            # checking same diagonal
            elif col_diff == row_diff:
                h+=1
    return h
# Generating neighbors
def neighbors(queen_positions):
    successors = []
    # looping i from 0 to 7
    for i in range(len(queen_positions)):
        # looping j from 0 to 7
        for j in range(len(queen_positions)):
            if j != queen_positions[i]:
                # making copy of original state
                copy = queen_positions.copy()
                # changing copy at element by j value
                copy[i] = j
                # adding new list to successors list
                successors.append(copy)
    return successors
# Standard Hill Climbing Algorithm
def standard_hill_climbing(initial_state):
    # initializing current state as the initial state
    curr_state = initial_state
    # infinite loop
    while True:
        # generating neighbors of current state
        successors = neighbors(curr_state)
        # initializing minimum heuristic state as the first element in successors list of lists
        min_successor = successors[0]
        # looping through every successor list in the successors list of lists
        for successor in successors:
            # getting heuristic of successor 
            heur = heuristic(successor)
            # checking to see if current successor heuristic value is less than minimum heuristic value
            if heur < heuristic(min_successor):
                min_successor = successor
            # checking if the two heuristic values are the same
            elif heur == heuristic(min_successor):
                # creating list and adding the current and minimum successor
                ties = []
                ties.append(successor)
                ties.append(min_successor)
                # randomly choosing between the two equal successors
                min_successor = random.choice(ties)
        # checking if the minimum cost value of successors is greater than current cost to return state
        if heuristic(min_successor) >= heuristic(curr_state):
            return curr_state
        # if not the minimum successor becomes the current state
        curr_state = min_successor
# Counting the number of boards generated for hill climbing
def hill_num_boards(initial_state, boards):
    curr_state = initial_state
    num_boards = boards
    while True:
        successors = neighbors(curr_state)
        min_successor = successors[0]
        for successor in successors:
            heur = heuristic(successor)
            if heur < heuristic(min_successor):
                min_successor = successor
            elif heur == heuristic(min_successor):
                ties = []
                ties.append(successor)
                ties.append(min_successor)
                min_successor = random.choice(ties)
        if heuristic(min_successor) >= heuristic(curr_state):
            return num_boards
        # if the current state changes we add 1 to number of boards generated
        curr_state = min_successor
# Simulated Annealing Algorithm
def simulated_annealing(initial_state):
    # initializing current state as the initial state
    curr_state = initial_state
    # initializing temp at 4000
    t = 4000
    # As long as t is not close to 0
    while math.floor(t) != 0:
        # decaying temp at 0.99 rate 
        t = t * 0.99
        # randomly selecting successor out of all possible neighbors
        successor = random.choice(neighbors(curr_state))
        # calculating different between current heuristic value and successor heuristic value
        c = heuristic(curr_state) - heuristic(successor)
        # probability value to decrease chance of picking bad
        p = math.exp(-c/t)
        # randomly choosing between 0 and 1 with probability weights
        rand_num = random.choices([0,1], weights=[p, 1-p])
        # if heuristic difference is greater than 0 current state becomes successor
        if c > 0:
            curr_state = successor
        # if heuristic difference is less than 0 and random number generated is 0 current state becomes successor
        elif c < 0  and rand_num == 0: 
            curr_state = successor
    return curr_state
# Counting the number of boards generated for simulated annealing
def sim_num_boards(initial_state, boards):
    curr_state = initial_state
    num_boards = boards
    t = 4000
    while math.floor(t) != 0:
        t = t * 0.99
        successor = random.choice(neighbors(curr_state))
        c = heuristic(curr_state) - heuristic(successor)
        p = math.exp(-c/t)
        rand_num = random.choices([0,1], weights=[p, 1-p])
        if c > 0:
            curr_state = successor
            # if current state changes add 1 to number of boards
            num_boards+=1
        elif c < 0  and rand_num == 0: 
            curr_state = successor
            # if current state changes add 1 to number of boards
            num_boards+=1
    return num_boards
# number of puzzles read in from command line
num_puzzles = int(sys.argv[1])
# initializing the number of solutions for each algorithm to 0
hill_solutions = 0
simulated_solutions = 0
# initializing the number of boards generated for each algorithm to 0
hill_boards = 0
simulated_boards = 0
# looping through each puzzle based on num_puzzles values
for puzzle in range(0,num_puzzles):   
    # initialzing 8 element list of queen positions with element position as columns and values as rows
    queen_pos = []
    for i in range(0,8):
        # randomly adding numbers from 0 to 7 to each element of queen_pos list
        queen_pos.append(random.choice(range(0,8))) 
    # capturing heuristic value of hill climbing algorithm
    hill_climbing_heuristic = heuristic(standard_hill_climbing(queen_pos))
    # capturing heuristic value of simulated annealing algorithm
    simulated_annealing_heuristic = heuristic(simulated_annealing(queen_pos))
    # storing number of boards by adding to previous amount for each puzzle iteration
    hill_boards += hill_num_boards(queen_pos, 0)
    simulated_boards += sim_num_boards(queen_pos, 0)
    # storing number of solutions per algorithm by checking if heuristic value equals 0
    if hill_climbing_heuristic == 0:
        hill_solutions += 1
    if simulated_annealing_heuristic == 0:
        simulated_solutions += 1
   
# End Message 
print(num_puzzles, "puzzles.")
print("Std. Hill-Climbing:", round((hill_solutions / num_puzzles) * 100), "%", "solved, average search cost: ", hill_boards / num_puzzles)
print("Sim. Annealing:", round((simulated_solutions / num_puzzles) * 100), "%", "solved, average search cost: ", simulated_boards / num_puzzles)

    


# # 

# In[ ]:





# In[ ]:




