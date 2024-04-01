#!/usr/bin/env python
# coding: utf-8

# In[88]:


import pandas as pd
import warnings
import re
import numpy as np
import time

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'
warnings.simplefilter(action='ignore', category=FutureWarning)


# ### Select Scouts

# Choose scouts

# In[100]:


def set_scouts():
    global not_yet_scouted
    
    #-------------- get list of scoutable teams ------------------#
    scoutable_teams = pd.read_csv("Actions/Extra_actions.csv").set_index("ID") # get teams available to be scouted
    already_scouted = pd.read_csv("Scouts/Scouted so far.csv").set_index("ID") # get teams already scouted
    not_yet_scouted = pd.concat([already_scouted,scoutable_teams]).drop_duplicates(keep=False) # concat both lists and get rid of all duplicates to avoid scouting a team twice

    #--------------- get countries ------------------#
    not_yet_scouted["Country"] = not_yet_scouted["TEA Random"].str.split().str[-1] # get last word of column and set as the country
    countries = not_yet_scouted.groupby("Country") # create new group based on extra action countries
    x=0


    while x == 0:
        country_select = input("Which country would you like to scout from? " ) # select country to draw scouts from
        
        scout_no = input("How many teams would you like to scout this week?")
        
        # return list of scouts as defined by the input - state if chosen country is not scoutable
        if country_select in countries.groups.keys():
            scout_teams = countries.get_group(country_select)
            global MDS_scouts
        
            if scout_teams.empty:
                MDS_scouts = pd.DataFrame()
            else:
                try:
                    MDS_scouts = scout_teams.sample(n=int(scout_no)) # get 10 random scoutable teams from those that haven't been scouted yet
                                   
                    write_scouts = MDS_scouts.drop(columns = ["Country"])
    
                    overwrite_scouts = pd.concat([already_scouted,write_scouts])
                    overwrite_scouts.drop_duplicates(subset=["TEA Random"],inplace=True)
                    overwrite_scouts.to_csv("Scouts/Scouted so far.csv", mode="w")
                    write_scouts.to_csv("Scouts/Scouted this week.csv")
                    time.sleep(1)
                    print("\n" + country_select + " selected. Writing scouts to file...")
                    time.sleep(1)
                    print("\n Teams chosen are...")
                    time.sleep(1)
                    print(write_scouts)
                    time.sleep(1)
                    print("\n Write complete.")
                    time.sleep(5)
                    x=1
                    break
                except:
                    time.sleep(1)
                    
                    print("Not enough teams to draw from. Please select a different country.")
                    time.sleep(2)
                    continue
        elif country_select not in countries.groups.keys():
            print("Country not scoutable")
            time.sleep(1)
            print("Please check spelling and try again")
            time.sleep(1)
            continue
    else:
        pass
    


set_scouts()


# In[ ]:




