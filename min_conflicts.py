#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
"""Assignment 5 (8 Queens with min conflicts) """
_author_ = "Alex Lagarde"

# importing libraries 
import random
import sys
import math
# function computing heuristic of board with board as parameter
def heuristic(queen_positions):
    # initializing the board to parameter and heuristic value to 0
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
    # returning heuristic value
    return h
# function to calculate the number of conflicts to the right of a queen with board and specified column as parameters
def col_conflicts_above(queen_positions, ele):
    # intializing the board to parameter, the specified column to parameter, and the specified number of conflicts for one column to 0
    board = queen_positions
    column = ele
    h = 0
    # looping through each column from the intial column to the last column to the right of it
    for col in range(column + 1, len(board)):
        # calculating the absolute value of the differences of columns and rows to help calculate diagonal conflicts
        col_diff = abs(col - column)
        row_diff = abs(board[column] - board[col])
        # checking horizontal conflicts
        if board[column] == board[col]:
            h+=1
        # checking diagonal conflicts
        elif col_diff == row_diff:
            h+=1
    # returning number of conflicts for a specific queen to the right
    return h        
# function to calculate the number of conflicts to the left of a queen with board and specified column as parameters
def col_conflicts_below(queen_positions, ele):
    # intializing the board to parameter, the specified column to parameter, and the specified number of conflicts for one column to 0
    board = queen_positions
    column = ele 
    h = 0
    # looping through each column from the intial column to the last column to the right of it
    for col in range(column - 1, -1, -1):
        # calculating the absolute value of the differences of columns and rows to help calculate diagonal conflicts
        col_diff = abs(col - column)
        row_diff = abs(board[column] - board[col])
        # checking horizontal conflicts
        if board[column] == board[col]:
            h+=1
        # checking diagonal conflicts
        elif col_diff == row_diff:
            h+=1
    # returning number of conflicts for a specific queen to the left
    return h 
# function to return successors with board and specified column as parameters
def successors(queen_positions,curr_col):
    # initializing the board to parameter, the column to parameter, and the empty list of successors
    board = queen_positions
    col = curr_col
    successors = []
    # looping through all the possible row positions for successors
    for j in range(len(queen_positions)):
        # if the row is different than the original row, the add the new board to successors
        if j != queen_positions[col]:
            # making copy of original state
            copy = queen_positions.copy()
            # changing copy at element by j value
            copy[col] = j
            # adding new list to successors list
            successors.append(copy)
    # return list of lists for the 7 successors
    return successors
# min conflicts algorithm with the board and max number of steps as parameters            
def min_conflicts(queen_positions, max):
    # initializing board and max steps to parameters
    board = queen_positions
    max_steps = max
    # initializing times search stuck, times reaching a global/local minimum, and boards searched to 0
    times_stuck = 0
    local_global_minimums = 0
    boards_searched = 0
    # looping through each step until max steps is reached
    for step in range(max_steps):
        # everytime we loop through we search one board
        boards_searched+=1
        # we check heuristic value and if 0, a global minimum is reached and we return 
        if heuristic(board) == 0:
            local_global_minimums+=1
            # return in a tuple: the board, the times program gets stuck, the number of boards searched, and number of local and global minimums reached
            return board, times_stuck, boards_searched, local_global_minimums
        # creating dictionary with key as index or column and value as the row position
        queen_conflicts = {}
        # creating list for keys that are unsubscriptable
        column_conflicts =[]
        # looping through each column
        for col in range(8):
            # if the sum of conflicts to the right and conflicts to the left is greater than 0, there is a conflict
            if col_conflicts_above(board, col) + col_conflicts_below(board, col) > 0:
                # adding the column and row position to the dictionary
                queen_conflicts.update({col : board[col]})
        # adding keys of dictionary to list to make them subscriptable
        for i in queen_conflicts.keys():
            column_conflicts.append(i)
        # randomly selecting column from columns in conflict
        curr_col = random.choice(column_conflicts)
        # generating list of lists of successors
        children = successors(board, curr_col)
        # saving number of conflicts of current conflicting queen column
        curr_conflicts = col_conflicts_above(board, curr_col) + col_conflicts_below(board, curr_col)
        # initializing lowest number of conflicts value to current
        lowest_conflicts = col_conflicts_above(board, curr_col) + col_conflicts_below(board, curr_col)
        # creating empty new board
        new_board = []
        # looping through each successor
        for child in children:
            # adding 1 to boards searched
            boards_searched+=1
            # saving number of conflicts value of successor
            num_conflicts = col_conflicts_above(child, curr_col) + col_conflicts_below(child, curr_col)
            # checking if lower than lowest value
            if num_conflicts < lowest_conflicts:
                # saving lowest value as current successor heuristic value
                lowest_conflicts = num_conflicts
                # saving new board as current successor
                new_board = child
                # if lowest conflicts value is 0 now, we exit for loop
                if lowest_conflicts == 0:
                    break
        # if the lowest heuristic value is equivalent to current board heuristic, we reached local minimum and program is stuck
        if curr_conflicts == lowest_conflicts:
            # randomize which successor is chosen
            board = random.choice(children)
            times_stuck+=1 
            local_global_minimums+=1
        else:
            # replace board with new board
             board = new_board 
    # return in a tuple: a failure if we go through all the steps, the times program gets stuck, the number of boards searched, and number of local and global minimums reached   
    return "failure", times_stuck, boards_searched, local_global_minimums

# number of puzzles read in from command line
num_puzzles = int(sys.argv[1])
# initializing the number of solutions, times the program gets stuck, boards searched, local and global minimums reached to 0
solutions = 0
num_search_stuck = 0
num_boards_searched = 0
local_global_minimums_reached = 0
# looping through each puzzle
for puzzle in range(0,num_puzzles):   
    # initialzing 8 element list of queen positions with element position as columns and values as rows
    queen_pos = []
    for i in range(0,8):
        # randomly adding numbers from 0 to 7 to each element of queen_pos list
        queen_pos.append(random.choice(range(0,8))) 
    # save the tuple returned from min conflicts algorithm with a max number of steps of 4000 to an object
    result_tuple = min_conflicts(queen_pos, 4000)
    # checking if the first element returns a failure
    if result_tuple[0] != "failure" :
        # if it is not a failure than it is a solution so we add 1
        solutions+=1
    # cumulatively adding the number of times the search got stuck, the number of boards searched, the number of local and global maximums reached
    num_search_stuck+=result_tuple[1]
    num_boards_searched+=result_tuple[2]
    local_global_minimums_reached+=result_tuple[3]
    
# End Message 
print(num_puzzles, "puzzles.")
print("Min-conflicts:", round((solutions / num_puzzles) * 100), "%", "solved")
print("Average Search Cost: ", num_boards_searched / local_global_minimums_reached)
print("Average Times Stuck: ", num_search_stuck / num_puzzles)

# Description:
# Program takes in a number of puzzles, generates random boards, calls the min conflicts algorithm, which returns a tuple, 
# and outputs the percentage of puzzles solved, the average search cost, and the average times the program gets stuck. Although I cannot  
# tell whether the search cost is better because my search cost in assignment 4 was wrong, the min conflicts algorithm outperforms
# the simulated annealing and hill climbing algorithms since the min conflicts algorithm, correctly solves the problem essentially 100% 
# of the time with a max steps of 4000, which is similar to simulated annealing's temperature parameter, while hill climbing and 
# simulated annealing are less than 20% solved. 