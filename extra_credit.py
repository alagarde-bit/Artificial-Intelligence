#!/usr/bin/env python
# coding: utf-8

# In[13]:


## Your name here: Alex Lagarde
## Source code is from https://www.datacamp.com/community/tutorials/introduction-reinforcement-learning

# DIRECTIONS
# The code below will run the 10 armed bandit problem - and example of
# reinforcement learning. Some comments are already included.
#
# Using our discussion in class, the article, and online search - add
# your own comments explaining how each line of code works toward solving this
# problem.
#
#Also write a longer description above each method to explain how it
# works in general.

# reading in libraries
import numpy as np
import random
import matplotlib.pyplot as plt
import timeit
#%matplotlib inline
start = timeit.default_timer()
# sets random seed to 5, which saves the sequence of random numbers to help with reproducibility
np.random.seed(5)
# the 10 different possible arms
n = 10
# randomly fills in values from 0 to 1, which represent probabilities, for all 10 arms 
arms = np.random.rand(n)
# prints the numpy array
print("arms", arms)
eps = 0.1 #probability of exploration action

# each arm will run loop through 10 iterations of random numbers from 0 to 1. 
# if the arm probability is greater than the random probability the reward increases by 1
def reward(prob):
    # initializing reward to 0
    reward = 0
    # looping through from 0 to 9 or 10 iterations
    for i in range(10):
        # checking if the randomly generated number is less than arm probability
        if random.random() < prob:
            # adding 1 if condition is true
            reward += 1
    # returning new reward value for that arm after the 10 iterations
    return reward

# initialize memory array; has 1 row defaulted to random action index
av = np.array([np.random.randint(0,(n+1)), 0]).reshape(1,2) #av = action-value
times = np.zeros(11)

#greedy method to select best arm takes in memory array that 
def bestArm(a):
    # initializing best arm to 0
    bestArm = 0 
    # initializing best mean to 0
    bestMean = 0
    # looping through elements in numpy array
    for u in a:
        # taking mean of rewards where the a element equals u
        avg = u[1] #calculate mean reward for each action
        # if best mean is less than avg best mean becomes avg
        if bestMean < avg:
            bestMean = avg
            # best arm becomes the index
            bestArm = u[0]
    # returns the best arm after looping through numpy array
    return bestArm

# labeling x axis of graph: Number of times played
plt.xlabel("Number of times played")
# labeling y axis of graph: Average Reward
plt.ylabel("Average Reward")
# looping 500 times from 0 to 499
total_iterations = 0
runningMean = 0
for i in range(500):
    reward_val = 0
    total_iterations+=1
    # if random number is greater than eps
    if random.random() > eps: #greedy exploitation action
        # choice becomes best arm of the action value memory array
        choice = bestArm(av)
        times[choice] += 1
        if choice not in av[:, 0]:
            reward_val = reward(arms[choice])
            thisAV = np.array([[choice, reward_val]])
            av = np.concatenate((av, thisAV), axis=0)
        else:
            for action in av:
                if action[0] == choice:
                    reward_val =  reward(arms[choice])
                    action[1] = action[1] + ((reward_val- action[1])/ times[choice])
                    break
    else: #exploration action
        choice = np.where(arms == np.random.choice(arms))[0][0]
        times[choice] += 1
        # make new 1 by 2 array with the best arm and reward of that arm
        if choice not in av[:, 0]:
            reward_val = reward(arms[choice])
            thisAV = np.array([[choice, reward_val]]) 
            av = np.concatenate((av, thisAV), axis=0) 
        else: 
            for action2 in av:
                if action2[0] == choice:
                    reward_val = reward(arms[choice])
                    action2[1] = action2[1] + ((reward_val- action2[1]) / times[choice])
                    break 
    #calculate the mean reward
    runningMean = runningMean + ((reward_val - runningMean) / total_iterations)
    # creating a scatter plot with i on x and running mean on y
    plt.scatter(i, runningMean)
    
end = timeit.default_timer()
print("Time:", end - start)


# In[ ]:





# In[ ]:




