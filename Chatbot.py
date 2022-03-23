#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # -*- coding: utf-8 -*-
""" Eliza homework. Relationship advisor """
__author__="Alex Lagarde"


# In[2]:


# importing libraries
import re
import random


# In[ ]:


name_patterns = [
    re.compile("my name is (.*)\.?", re.IGNORECASE),
    re.compile("I am (.*)\.?", re.IGNORECASE),
    re.compile("(.*) is my name", re.IGNORECASE),
    re.compile("I like to be called (.*)\.?", re.IGNORECASE),
    re.compile("I'm (.*)\.?", re.IGNORECASE),
    re.compile("I am called (.*)\.?", re.IGNORECASE),
    re.compile("I'm called (.*)\.?", re.IGNORECASE),
    re.compile("I was named (.*)\.?", re.IGNORECASE),
    re.compile("(.*) is how I am called", re.IGNORECASE),
    re.compile("My name's (.*)\.?", re.IGNORECASE),
    re.compile("Mine is (.*)\.?", re.IGNORECASE),
    re.compile("Mine's (.*)\.?", re.IGNORECASE),
    re.compile("This is (.*)\.?", re.IGNORECASE)]

feel_patterns = [
    re.compile("I feel (.*)\.?", re.IGNORECASE),
    re.compile("I am (.*)\.?", re.IGNORECASE),
    re.compile("I'm (.*)\.?", re.IGNORECASE),
    re.compile("I am doing (.*)\.?", re.IGNORECASE),
    re.compile("I'm doing (.*)\.?", re.IGNORECASE),
    re.compile("I am feeling (.*)\.?", re.IGNORECASE),
    re.compile("I'm feeling (.*)\.?", re.IGNORECASE),
    re.compile("Pretty (.*)\.?", re.IGNORECASE),
    re.compile("Not too (.*)\.?", re.IGNORECASE),
    re.compile("Doing (.*)\.?", re.IGNORECASE),
    re.compile("Not (.*)\.?", re.IGNORECASE),
    re.compile("Just (.*)\.?", re.IGNORECASE),
    re.compile("I am mostly (.*)\.?", re.IGNORECASE),
    re.compile("I'm mostly (.*)\.?", re.IGNORECASE),
    re.compile("I am so (.*)\.?", re.IGNORECASE),
    re.compile("I am very (.*)\.?", re.IGNORECASE),
    re.compile("I am kind of (.*)\.?", re.IGNORECASE),
    re.compile("Mostly (.*)\.?", re.IGNORECASE),
    re.compile("Kind of (.*)\.?", re.IGNORECASE),
    re.compile("Sort of (.*)\.?", re.IGNORECASE),
    re.compile("I am sort of (.*)\.?", re.IGNORECASE),
    re.compile("Feeling (.*)\.?", re.IGNORECASE),
    re.compile("I'm so (.*)\.?", re.IGNORECASE),
    re.compile("I'm sort of (.*)\.?", re.IGNORECASE),
    re.compile("I'm kind of (.*)\.?", re.IGNORECASE),
    re.compile("I'm very (.*)\.?", re.IGNORECASE),
    re.compile("So (.*)\.?", re.IGNORECASE)
    
]
good_synonyms = ["good", 
                 "well",
                 "awesome",
                 "fantastic",
                 "excellent",
                 "solid",
                 "exceptional",
                 "wonderful",
                 "marvelous",
                 "superb",
                 "spectacular",
                 "tremendous",
                 "phenomenal",
                 "incredible",
                 "great",
                 "nice"
]
happy_synonyms = ["happy",
                  "joyful",
                  "jovial",
                  "delighted",
                  "content"   
]
angry_synonyms = ["angry",
                 "frustrated",
                  "annoyed",
                  "irate",
                  "irritated",
                  "aggravated"  
]
sad_synonyms = ["sad",
               "saddened",
               "depressed",
               "miserable",
               "unhappy"
               ]

okay_synonyms = ["okay",
                "alright",
                "fine",
                "ok",
                "decent"
]
bad_synonyms = ["bad",
               "awful",
               "horrific",
               "terrible",
                "poor",
                "crap",
                "shit"               
]
good_responses = [
    "That's great! Why are you {}?",
    "That's good! Why are you {}? ",
    "Happy for you! Why are you {}?",
    "That's amazing! Why are you {}?",
    "That's awesome! Why are you {}?",
    "Super! Why are you {}?", 
    "Incredible! Why are you {}?",
    "Nice! Why are you {}?"
]
okay_responses = [
    "Oh okay. How come are you just {}?",
    "Why is that you are just {}?",
    "Why just {}?",
    "Why not {}?"
]
bad_responses = [
    "Sorry to hear that. Why are you {}?",
    "Sorry you feel that way. Why are you {}?",
    "That is no fun. Why are you {}?",
    "Oh that's not good. Why are you {}?",
    "Must be hard for you. Why are you {}?",
    "I apologize you feel that way? Why are you {}?",
    "What happened? Why are you {}?"
]
while True:
    print("Hello, welcome to Relationship Advisors. What is your name? (type bye to end conversation)")
    nameString = input()
    if nameString.casefold() == 'bye':
        print('Thank you. Have a great day!')
        break
    elif len(nameString.split()) == 1:
        print('Hello,', nameString)
    else:
        for pattern in name_patterns:
            match = pattern.search(nameString) 
            if match:
                name = match.group(1)
                print('Hello,', name)
                break
        else:
            print("Could you please re-type your name?")
    print("How are you doing?")
    moodString = input().lower()
    if moodString.casefold() == 'bye':
        print('Thank you. Have a great day!')
        break
    elif len(moodString.split()) == 1 and moodString.casefold() in good_synonyms:
        print(random.choice(good_responses).format(moodString))
    elif len(moodString.split()) == 1 and moodString.casefold() in okay_synonyms:
        print(random.choice(okay_responses).format(moodString))
    elif len(moodString.split()) == 1 and moodString.casefold() in bad_synonyms:
        print(random.choice(bad_responses).format(moodString))
    elif len(moodString.split()) == 1 and moodString.casefold() in angry_synonyms:
        print(random.choice(bad_responses).format(moodString))
    elif len(moodString.split()) == 1 and moodString.casefold() in sad_synonyms:
        print(random.choice(bad_responses).format(moodString))
    elif len(moodString.split()) == 1 and moodString.casefold() in happy_synonyms:
        print(random.choice(good_responses).format(moodString))
    else:
        for pattern in feel_patterns:
            match = pattern.search(moodString)
            if (match and any(ele in good_synonyms for ele in moodString.split())) and "not" not in moodString.split():
                print(random.choice(good_responses))
                break
            elif (match and any(ele in okay_synonyms for ele in moodString.split())) and "not" not in moodString.split():
                print(random.choice(okay_responses))
                break
            elif (match and any(ele in bad_synonyms for ele in moodString.split())) and "not" not in moodString.split():
                print(random.choice(bad_responses))
                break  
            elif(match and any(ele in good_synonyms for ele in moodString.split())) and "not" in moodString.split():
                print(random.choice(bad_responses))
                break
            elif (match and any(ele in okay_synonyms for ele in moodString.split())) and "not" in moodString.split():
                print(random.choice(bad_responses))
                break
            elif (match and any(ele in bad_synonyms for ele in moodString.split())) and "not" in moodString.split():
                print(random.choice(okay_responses))
                break
            elif(match and any(ele in angry_synonyms for ele in moodString.split())):
                print(random.choice(bad_responses).format(ele))
                break
            elif(match and any(ele in sad_synonyms for ele in moodString.split())):
                print(random.choice(bad_responses).format(ele))
                break
            elif(match and any(ele in happy_synonyms for ele in moodString.split())):
                print()
        else:
            print("Could you clarify how you are?")
            break
    #verbs_ed =[]
   # actionString = input()
     #   for p in action.split():
        #    if p.endswith('ed'):
          #      infinitive = p[:-2]
          #      verbs_ed.append(infinitive)
          #  elif p.lower() == "mom" or p.lower() == "mother":
            #    print("")
   
    
    
    
    


# In[ ]:





# In[ ]:





# 
