#!/usr/bin/env python
# coding: utf-8

# In[15]:


# I worked with Kobie Williams
# importing random library to generate numbers from 0 to 7
import random
# creating list for the positions of queens
queen_pos = [1,2,3,4,5,6,7,8]
random.shuffle(queen_pos)
print(queen_pos)
# looping by row then column and adding queen where the column number equals the queen position and adding - if not
for i in range(0,8):
    for j in range(0,8):
        if j == queen_pos[i]:
            print('Q', end = ' ')
            # using end = ' ' so that it does not print a newline
        else:
            print('-', end=' ')
             # using end = ' ' so that it does not print a newline
    print()

