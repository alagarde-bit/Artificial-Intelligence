#!/usr/bin/env python
# coding: utf-8
""" AI Project. Stock Trader Bot """
__author__="Alex Lagarde"

# In[1]:


# required libraries
import numpy as np
import pandas as pd
import random


# In[62]:


# storing data in pandas dataframe
nvidia = pd.read_csv("NVDA.csv")
nvidia = nvidia['Open']
# sets random seed to 5, which saves the sequence of random numbers to help with reproducibility
np.random.seed(5)
#initializing state space
account_balance = 20000
nvidia_shares_owned = 0
nvidia_price = round(nvidia[0])
action_space = np.array(["buy", "sell", "hold"])

# initializing Q-Learning Parameters
q_table = np.zeros((1,3))
eps = 1.0
decay_rate = 0.01
min_eps = 0.1
# learning rate
alpha = 1
# discount rate
gamma = 1
episodes = len(nvidia.index)
total_rewards = 0
# initializing the initial state for nvidia stock
nvidia_state = np.array([nvidia_price, nvidia_shares_owned, account_balance]).reshape((1,3))
nvidia_state_space = nvidia_state.reshape((1,3))
# keeping track of rewards
episode_reward = 0
episode_iterations = 0
def nvidia_actions(state, action, episode, q_table, nvidia_state_space):
    # initializing parameters
    nvidia_state = state
    nvidia_action = action
    i = episode
    nvidia_q_table = q_table
    state_space = nvidia_state_space  
    if nvidia_action == "sell":
        # checking if the number of shares owned for the stock is 0 because selling is not possible
        if nvidia_state[0][1] == 0:
         # randomly choosing between buy and hold
         nvidia_action = np.random.choice(['buy', 'hold'])
        # checking if last episode making necessary updates and then printing
        elif i == episodes:
            # adjusting account balance after selling all stock by multiplying current stock price by number of shares sold and resetting shares owned to 0
            nvidia_state[0][2] += round(nvidia_state[0][0]) * nvidia_state[0][1]
            nvidia_state[0][1] = 0  
            # returning state, reward of 0 because unknown, q table, state space, and action taken
            return nvidia_state, 0, nvidia_q_table, state_space, nvidia_action
        else:
            # getting the next state
            nvidia_next_state = np.array([round(nvidia[i]), nvidia_state[0][1], nvidia_state[0][2]]).reshape((1,3))
            # adjusting account balance after selling and resetting shares owned to 0
            nvidia_next_state[0][2] += nvidia_state[0][0] * nvidia_next_state[0][1]
            nvidia_next_state[0][1] = 0 
            # checking if next state is already in state space
            if np.any(np.all(np.isin(state_space,nvidia_next_state,True),axis=1)):
                # calculating reward by difference of original value to next value because decrease after selling is good
                nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                # extracting the index in the state space by looping through to see if all row values match with a row in state space
                next_state_idx = 0
                current_state_idx = 0
                for j in np.arange(len(state_space)):
                    if state_space[j][0] == nvidia_state[0][0] and state_space[j][1] == nvidia_state[0][1] and state_space[j][2] == nvidia_state[0][2]:
                            current_state_idx = j
                            break
                for k in np.arange(len(state_space)):
                    if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                            next_state_idx = k
                            break
                # Bellman equation updating q table
                nvidia_q_table[current_state_idx, 1] = (1-alpha) * nvidia_q_table[current_state_idx, 1] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 1])
                # current state is the next state and returning state, reward, q table, state space, and action taken
                nvidia_state = nvidia_next_state
                return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
            # if state not in the state space
            else:
                # adding row to q table and state space for new state
                newq_table = np.zeros((1,3))
                nvidia_q_table = np.concatenate((nvidia_q_table, newq_table), axis = 0)
                state_space = np.concatenate((state_space, nvidia_next_state), axis = 0)  
                # calculating reward
                nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                # extracting indexes with next state being the last row now and current state being the second to last row
                next_state_idx = len(state_space) - 1
                current_state_idx = len(state_space) - 2
                # updating q table
                nvidia_q_table[current_state_idx, 1] = (1-alpha) * nvidia_q_table[current_state_idx, 1] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 1])                                                                              
                # updating state and returning state, reward, q table , and state space
                nvidia_state = nvidia_next_state 
                return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
    # checking if nvidia action is hold
    if nvidia_action == "hold":
        # checking if last episode and printing everything
        if i == episodes:
            return nvidia_state, 0, nvidia_q_table, state_space, nvidia_action
        else:
            # getting the next state and not updating anything because of hold except for the price
            nvidia_next_state = np.array([round(nvidia[i]), nvidia_state[0][1], nvidia_state[0][2]]).reshape((1,3))
            # checking if next state in state space
            if np.any(np.all(np.isin(state_space,nvidia_next_state,True),axis=1)):
                # checking if shares owned is 0
                if nvidia_state[0][1] == 0:
                    # calculating reward when owning no stock and adding to episode reward
                    nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                    # extracting index again
                    next_state_idx = 0
                    current_state_idx = 0
                    for j in np.arange(len(state_space)):
                        if state_space[j][0] == nvidia_state[0] and state_space[j][1] == nvidia_state[1] and state_space[j][2] == nvidia_state[2]:
                            current_state_idx = j
                            break
                    for k in np.arange(len(state_space)):
                        if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                            next_state_idx = k
                            break
                    # updating q table and changing state to next state
                    nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                    nvidia_state = nvidia_next_state  
                    return nvidia_state, nvidia_reward, nvidia_q_table, nvidia_state_space, nvidia_action
                else:
                    # calculating reward when owning stock and adding to episode reward
                    nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                    # extract indexing again
                    next_state_idx = 0
                    current_state_idx = 0
                    for j in np.arange(len(state_space)):
                        if state_space[j][0] == nvidia_state[0] and state_space[j][1] == nvidia_state[1] and state_space[j][2] == nvidia_state[2]:
                            current_state_idx = j
                            break
                    for k in np.arange(len(state_space)):
                        if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                            next_state_idx = k
                            break
                    # updating q table and changing state to next state
                    nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                    nvidia_state = nvidia_next_state
                    return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
            # state not seen
            else:
                # adding row to q table and state space for new state
                newq_table = np.zeros((1,3))
                nvidia_q_table = np.concatenate((nvidia_q_table, newq_table), axis = 0)
                state_space = np.concatenate((state_space, nvidia_next_state))
                # checking if no shares owned
                if nvidia_state[0][1] == 0:
                    # calculating reward when owning no stock and adding to episode reward
                    nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                    # extract indexes
                    current_state_idx = len(state_space) - 2
                    next_state_idx = len(state_space) - 1
                    # updating q table and changing state to next state
                    nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])                                                                              
                    nvidia_state = nvidia_next_state
                    return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
                # shares owned
                else:
                     # calculating reward when owning stock and adding to episode reward
                    nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                    # extract index
                    current_state_idx = len(state_space) - 2
                    next_state_idx = len(state_space) - 1
                    # updating q table and changing state to next state
                    nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])                                                                              
                    nvidia_state = nvidia_next_state
                    return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
    # checking if nvidia action was buy
    if nvidia_action == "buy":
        # checking if account balance is 0 because cannot buy if so
        if nvidia_state[0][2] == 0:
            # must choose between sell and hold randomly
            nvidia_action = np.random.choice(['sell', 'hold'])
            # if randomly chosen action was sell repeat sell condition from above expect no checking for stocks owned
            if nvidia_action == "sell":
                if i == episodes:
                    nvidia_state[0][2] += nvidia_state[0][0] * nvidia_state[0][1]
                    nvidia_state[0][1] = 0    
                    return nvidia_state, 0, nvidia_q_table, nvidia_state_space, nvidia_action
                else:
                    nvidia_next_state = np.array([round(nvidia[i]), nvidia_state[0][1], nvidia_state[0][2]]).reshape((1,3))
                    nvidia_next_state[0][2] += nvidia_next_state[0][0]* nvidia_state[0][1]
                    if np.any(np.all(np.isin(state_space,nvidia_next_state,True),axis=1)):
                        nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                        current_state_idx = 0
                        next_state_idx = 0
                        for j in np.arange(len(state_space)):
                            if state_space[j][0] == nvidia_state[0][0] and state_space[j][1] == nvidia_state[0][1] and state_space[j][2] == nvidia_state[0][2]:
                                current_state_idx = j
                                break
                        for k in np.arange(len(state_space)):
                            if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                                next_state_idx = k
                                break
                        nvidia_q_table[current_state_idx, 1] = (1-alpha) * nvidia_q_table[current_state_idx, 1] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 1])
                        nvidia_state = nvidia_next_state 
                        return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
                    else:
                        newq_table = np.zeros((1,3))
                        nvidia_q_table = np.concatenate((nvidia_q_table, newq_table), axis = 0)
                        state_space = np.concatenate((state_space, nvidia_next_state))                                                                                         
                        nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                        current_state_idx = len(state_space) - 2
                        next_state_idx = len(state_space) - 1
                        nvidia_q_table[current_state_idx, 1] = (1-alpha) * nvidia_q_table[current_state_idx, 1] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 1])                                                                              
                        nvidia_state = nvidia_next_state 
                        return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
            # randomly chosen action was hold. Repeat hold condition from above
            else:
                if i == episodes:
                    return nvidia_state, 0, nvidia_q_table, state_space, nvidia_action
                else:
                    nvidia_next_state = np.array([round(nvidia[i]), nvidia_shares_owned, account_balance]).reshape((1,3))
                    if np.any(np.all(np.isin(state_space,nvidia_next_state,True),axis=1)):
                        if nvidia_state[0][1] == 0:                                                                                        
                            nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                            next_state_idx = 0
                            current_state_idx = 0
                            for j in np.arange(len(state_space)):
                                if state_space[j][0] == nvidia_state[0][0] and state_space[j][1] == nvidia_state[0][1] and state_space[j][2] == nvidia_state[0][2]:
                                    current_state = j
                                    break
                            for k in np.arange(len(state_space)):
                                if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                                    next_state_idx = k
                                    break
                            nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                            nvidia_state = nvidia_next_state
                            return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
                        else:
                            nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                            next_state_idx = 0
                            current_state_idx = 0
                            for j in np.arange(len(state_space)):
                                if state_space[j][0] == nvidia_state[0][0] and state_space[j][1] == nvidia_state[0][1] and state_space[j][2] == nvidia_state[0][2]:
                                    current_state_idx = j
                                    break
                            for k in np.arange(len(state_space)):
                                if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                                    next_state_idx = k
                                    break
                            nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                            nvidia_state = nvidia_next_state 
                            return nvidia_state, nvidia_reward, nvidia_actions, state_space, nvidia_action
                    else:
                        newq_table = np.zeros((1,3))
                        nvidia_q_table = np.concatenate((nvidia_q_table, newq_table), axis = 0)
                        state_space = np.concatenate((state_space, nvidia_next_state), axis = 0)
                        if nvidia_state[0][1] == 0:                                                                                        
                            nvidia_reward = nvidia_state[0][0] - nvidia_next_state[0][0]
                            current_state_idx = len(state_space) - 2
                            next_state_idx = len(state_space) - 1
                            nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                            nvidia_state = nvidia_next_state 
                            return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
                        else:
                            nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                            current_state_idx = len(state_space) - 2
                            next_state_idx = len(state_space) - 1
                            nvidia_q_table[current_state_idx, 2] = (1-alpha) * nvidia_q_table[current_state_idx, 2] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:])) - nvidia_q_table[current_state_idx, 2])
                            nvidia_state = nvidia_next_state   
                            return nvidia_state, nvidia_reward, nvidia_state_space, state_space, nvidia_action
        # if episode equals last, buy as many shares as possible
        elif i == episodes:
            # dividing account balance by current stock price to get shares bought
            nvidia_shares_bought = nvidia_state[0][2] // nvidia_state[0][0]                                                                                 
            nvidia_state[0][1] += nvidia_shares_bought
            # account balance subtracted by stock price multiplied by shares bought
            nvidia_state[0][2] -= nvidia_state[0][0] * nvidia_shares_bought
            return nvidia_state, 0, nvidia_q_table, state_space, nvidia_action
        else:
            # generating next state
            nvidia_next_state = np.array([round(nvidia[i]),nvidia_state[0][1], nvidia_state[0][2]]).reshape((1,3))
            nvidia_shares_bought = nvidia_next_state[0][2] // nvidia_state[0][0]                                                                                  
            nvidia_next_state[0][1] += nvidia_shares_bought
            nvidia_next_state[0][2] -= nvidia_state[0][0] * nvidia_shares_bought
            # checking if next state in state space
            if np.any(np.all(np.isin(state_space,nvidia_next_state,True),axis=1)):
                # calculating reward by difference of next state and current state to see if price increased
                nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                next_state_idx = 0
                current_state_idx = 0
                for j in np.arange(len(state_space)):
                    if state_space[j][0] == nvidia_state[0] and state_space[j][1] == nvidia_state[1] and state_space[j][2] == nvidia_state[2]:
                        current_state_idx = j
                        break
                for k in np.arange(len(state_space)):
                    if state_space[k][0] == nvidia_next_state[0][0] and state_space[k][1] == nvidia_next_state[0][1] and state_space[k][2] == nvidia_next_state[0][2]:
                        next_state_idx = k
                        break    
                nvidia_q_table[current_state_idx, 0] = (1-alpha) * nvidia_q_table[current_state_idx, 0] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:]) - nvidia_q_table[current_state_idx, 0]))                                                                              
                nvidia_state = nvidia_next_state 
                return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
            else:
                newq_table = np.zeros((1,3))
                nvidia_q_table = np.concatenate((nvidia_q_table, newq_table), axis = 0)
                state_space = np.concatenate((state_space, nvidia_next_state), axis = 0)
                nvidia_reward = nvidia_next_state[0][0] - nvidia_state[0][0]
                next_state_idx = len(state_space) - 1
                current_state_idx = len(state_space) - 2
                nvidia_q_table[current_state_idx, 0] = (1-alpha) * nvidia_q_table[current_state_idx, 0] + alpha*(nvidia_reward + gamma*(np.max(nvidia_q_table[next_state_idx,:]) - nvidia_q_table[current_state_idx, 0]))                                                                              
                nvidia_state = nvidia_next_state 
                return nvidia_state, nvidia_reward, nvidia_q_table, state_space, nvidia_action
# Q-Learning Algorithm 
# Looping through each day of trading
for i in np.arange(1, episodes):
    print(len(nvidia_state_space))
    # increasing the episode iterations by 1
    episode_iterations += 1
    # checking for exploitation if eps less than a random number 
    if eps < np.random.random():
        p
        if np.any(np.all(np.isin(nvidia_state_space,nvidia_state,True),axis=1)):
            idx = 0
            print(idx)
            for t in np.arange(len(nvidia_state_space)):
                if nvidia_state_space[t][0] == nvidia_state[0][0] and nvidia_state_space[t][1]== nvidia_state[0][1] and nvidia_state_space[t][2] == nvidia_state[0][2]:
                    idx = t
            nvidia_best = np.argmax(q_table[idx, :])
            nvidia_action = action_space[nvidia_best]
            result_tuple = nvidia_actions(nvidia_state, nvidia_action, i, q_table, nvidia_state_space)
            nvidia_state = result_tuple[0]
            episode_reward += result_tuple[1]
            q_table = result_tuple[2]
            nvidia_state_space = result_tuple[3]
            
        else:
            nvidia_action = np.random.choice(action_space)
            result_tuple = nvidia_actions(nvidia_state, nvidia_action, i, q_table, nvidia_state_space)
            nvidia_state = result_tuple[0]
            episode_reward += result_tuple[1]    
            q_table = result_tuple[2]
            nvidia_state_space = result_tuple[3]
    # exploration
    else:
        nvidia_action = np.random.choice(action_space)
        print("Original State:", nvidia_state)
        print("Action Told:", nvidia_action)
        result_tuple = nvidia_actions(nvidia_state, nvidia_action, i, q_table, nvidia_state_space)
        nvidia_state = result_tuple[0]
        episode_reward += result_tuple[1]
        q_table = result_tuple[2]
        nvidia_state_space = result_tuple[3]
        print("New State:", nvidia_state)
        print("Action Taken:", result_tuple[4])
        print("New qtable:", q_table)
        print("New State Space:", nvidia_state_space)
    # calculating average episode reward by dividing sum over episode iterations
    episode_reward = episode_reward / episode_iterations
    # updating eps using decay rate and making sure it does not go below minimum of 0.1
    eps = max(min_eps, eps*np.exp(-decay_rate*i))
    print("episode reward", episode_reward)
    print("epsilon value:", eps)
# sum all average rewards together
total_rewards += episode_reward * episode_iterations 
print("Total Rewards:", total_rewards)


# In[ ]:




