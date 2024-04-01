#!/usr/bin/env python
# coding: utf-8

# #### Imports

# In[13]:


import pandas as pd
import warnings
import re
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
import openpyxl

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'
warnings.simplefilter(action='ignore', category=FutureWarning)


# #### UE App Class

# In[14]:


# ================================================== UE APP ================================================== #

class UEApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1200x800")
        self.frames = {}

        
        for F in (First, Reserves, Youths):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(First)
        self.title("Ultimate Europe - Entirely Unofficial Companion")
       
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ======================================================================================================================= #
# ================================================== SUBMIT FIRST TEAM ================================================== #
# ======================================================================================================================= #
    
    def submit_first_team(self, players, positions, tactics, roles, roles_df, ticks, training, actions, names, password, formation, message):
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form.htm") # get the web address

        #=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
        
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = gks.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,1:2].squeeze(); SUB1_name = SUB1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);

        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)
        
        # tactics
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
        driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])
        driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        # training
        driver.find_element(By.NAME, "train").send_keys(training[0])
        driver.find_element(By.NAME, "train2").send_keys(training[1])
        driver.find_element(By.NAME, "train3").send_keys(training[2])
        driver.find_element(By.NAME, "train4").send_keys(training[3])
        driver.find_element(By.NAME, "train5").send_keys(training[4])
        driver.find_element(By.NAME, "train6").send_keys(training[5])
        driver.find_element(By.NAME, "train7").send_keys(training[6])
        driver.find_element(By.NAME, "train8").send_keys(training[7])
        driver.find_element(By.NAME, "train9").send_keys(training[8])
        driver.find_element(By.NAME, "train10").send_keys(training[9])

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        act6 = roles_df.query('Name == "'+ names[5] +'"'); action_id6 = act6.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id6").send_keys(action_id6); 
        driver.find_element(By.NAME, "action_name6").send_keys(names[5]); 
        driver.find_element(By.NAME, "action6").send_keys(actions[5])

        act7 = roles_df.query('Name == "'+ names[6] +'"'); action_id7 = act7.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id7").send_keys(action_id7); 
        driver.find_element(By.NAME, "action_name7").send_keys(names[6]); 
        driver.find_element(By.NAME, "action7").send_keys(actions[6])

        act8 = roles_df.query('Name == "'+ names[7] +'"'); action_id8 = act8.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id8").send_keys(action_id8); 
        driver.find_element(By.NAME, "action_name8").send_keys(names[7]); 
        driver.find_element(By.NAME, "action8").send_keys(actions[7])

        act9 = roles_df.query('Name == "'+ names[8] +'"'); action_id9 = act9.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id9").send_keys(action_id9); 
        driver.find_element(By.NAME, "action_name9").send_keys(names[8]); 
        driver.find_element(By.NAME, "action9").send_keys(actions[8])

        act10 = roles_df.query('Name == "'+ names[9] +'"'); action_id10 = act10.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id10").send_keys(action_id10); 
        driver.find_element(By.NAME, "action_name10").send_keys(names[9]); 
        driver.find_element(By.NAME, "action10").send_keys(actions[9])

        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        choochoo = pd.DataFrame({"Training":training})
        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    

        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            choochoo.to_excel(writer, sheet_name="training",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)
            
        get_scouts = pd.read_csv("Scouts/Scouted this week.csv")
        scouts = get_scouts["TEA Random"].tolist()

        
        # append scouts
        driver.find_element(By.NAME, "extra").send_keys(scouts[0])
        driver.find_element(By.NAME, "extra2").send_keys(scouts[1])
        driver.find_element(By.NAME, "extra3").send_keys(scouts[2])
        driver.find_element(By.NAME, "extra4").send_keys(scouts[3])
        driver.find_element(By.NAME, "extra5").send_keys(scouts[4])
        driver.find_element(By.NAME, "extra6").send_keys(scouts[5])
        driver.find_element(By.NAME, "extra7").send_keys(scouts[6])
        driver.find_element(By.NAME, "extra8").send_keys(scouts[7])
        driver.find_element(By.NAME, "extra9").send_keys(scouts[8])
        driver.find_element(By.NAME, "extra10").send_keys(scouts[9])

        # select same tactics
        if ticks[0] == 1:
            driver.find_element(By.NAME, "tactic722").click()
        else:
            pass
        if ticks[1] == 1:
            driver.find_element(By.NAME, "tactic723").click()
        else:
            pass
            
        driver.find_element(By.NAME, "textfield").send_keys(message) # enter message
        
        driver.find_element(By.NAME, "password").send_keys("password123") # enter password

# ======================================================================================================================= #    
# ================================================== SUBMIT RESERVE TEAM ================================================== #
# ======================================================================================================================= #    
    def submit_res_team(self, players, positions, tactics, roles, roles_df, actions, names, password,formation):
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form4.htm") # get the web address

#=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="r_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="r_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="r_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="r_att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
        
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = gks.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,1:2].squeeze(); SUB1_name = SUB1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);
        
        # tactics
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
        driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])
        driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        driver.find_element(By.NAME, "password").send_keys(password) # enter password
        

        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    
        
        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        
        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Res Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)

# ======================================================================================================================= #    
# ================================================== SUBMIT YOUTH TEAM ================================================== #
# ======================================================================================================================= #    
    def submit_yth_team(self, players, positions, tactics, roles, roles_df, actions, names, password, formation):
        print(f'Rxd formation is {formation}')
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form5.htm") # get the web address

#=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="y_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="y_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="y_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="y_att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
            
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = gks.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,1:2].squeeze(); SUB1_name = SUB1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);
        
        # tactics
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
        driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])
        driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        driver.find_element(By.NAME, "password").send_keys(password) # enter password
        
        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    
        
        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        
        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Yth Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)

    
# ================================================== ENABLE SUBMIT BUTTONS ================================================== #

    def enable_first_submit(self):
        for frame in self.frames.values():
            if isinstance(frame, (First)):
                frame.enable_first_submit()
                
    def enable_res_submit(self):
        for frame in self.frames.values():
            if isinstance(frame, (Reserves)):
                frame.enable_res_submit()


# #### First Team Class

# In[15]:


# ======================================================================================================================= #  
# =================================================== FIRST TEAM ======================================================== #
# ======================================================================================================================= #  
class First(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  # Store the controller instance
        self.config(bg="lightblue")


        # ============== STYLE =============== #
        
        # This will create style object
        style = ttk.Style()
        
        # Label style
        style.configure('Label', font = ('calibri', 10), foreground = 'black', background = "lightblue")
        # checkbox style
        style.configure("TCheckbutton", indicatorbackground="black", indicatorforeground="white",
                background="lightblue", foreground="black")
        # Title
        title = ttk.Label(self, text="First Team", style='Label')
        title.grid(row=1, column=1,pady=10, padx=10)
        
        # reserve button
        button1 = ttk.Button(self, text="Reserves", command=lambda: controller.show_frame(Reserves))
        button1.grid(row=2, column=1,pady=10, padx=10)

        # youth button
        button2 = ttk.Button(self, text="Youths", command=lambda: controller.show_frame(Youths))
        button2.grid(row=2, column=2,pady=10, padx=10)
        
        # set filepaths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Sub.xlsx"
        # get pd dfs
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file,"rb"), sheet_name="gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="att")
        DFA = pd.concat([deff,mid,att])

       # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only

        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist();
        Deff_names = deff['Name'].tolist(); 
        Mid_names = mid['Name'].tolist(); 
        Att_names = att['Name'].tolist(); 
        all_players = GK_names + Deff_names + Mid_names + Att_names
        
        # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar(); PL3 = StringVar(); PL4 = StringVar(); PL5 = StringVar(); PL6 = StringVar(); PL7 = StringVar(); PL8 = StringVar(); PL9 = StringVar(); PL10 = StringVar(); PL11 = StringVar() # store player names
        Pos2 = StringVar(); Pos3 = StringVar(); Pos4 = StringVar(); Pos5 = StringVar(); Pos6 = StringVar(); Pos7 = StringVar(); Pos8 = StringVar(); Pos9 = StringVar();Pos10 = StringVar(); Pos11 = StringVar()  # store positions
        sub1 = StringVar(); sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar(); # store sub names
        
        #------------- GK drop downs --------------#
        GK_txt = ttk.Label(self,text ='Goalkeeper',style="Label"); GK_txt.grid(row=5, column=1,pady=(10,0), padx=0)
        PL1_btn = ttk.OptionMenu(self, PL1, *GK_names, GK_names[0]); PL1.set(GK_names[0]);PL1_btn.grid(row=5, column=2,pady=(10,0), padx=0) # button to choose GK
        
        #------------- Defender drop downs --------------#
        P2_txt = ttk.Label(self,text ='Defender 1',style="Label"); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ttk.OptionMenu(self, PL2, *Deff_names,Deff_names[0]); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ttk.Label(self,text ='Position',style="Label"); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ttk.OptionMenu(self, Pos2, *deff_pos, deff_pos[0]); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ttk.Label(self,text ='Defender 2',style="Label"); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ttk.OptionMenu(self, PL3, *Deff_names,Deff_names[0]); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ttk.OptionMenu(self, Pos3, *deff_pos, deff_pos[0]); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ttk.Label(self,text ='Defender 3',style="Label"); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ttk.OptionMenu(self, PL4, *Deff_names,Deff_names[0]); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ttk.OptionMenu(self, Pos4, *deff_pos, deff_pos[0]); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ttk.Label(self,text ='Defender 4',style="Label"); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ttk.OptionMenu(self, PL5, *Deff_names,Deff_names[0]); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ttk.OptionMenu(self, Pos5, *deff_pos, deff_pos[0]); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ttk.Label(self,text ='Midfielder 1',style="Label"); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ttk.OptionMenu(self, PL6, *Mid_names,Mid_names[0]); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ttk.Label(self,text ='Position',style="Label"); Pos6_txt.grid(row=10,column=3,pady=(10,0))
        PL6_pos = ttk.OptionMenu(self, Pos6, *mid_pos, mid_pos[0]); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ttk.Label(self,text ='Midfielder 2',style="Label"); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ttk.OptionMenu(self, PL7, *Mid_names,Mid_names[0]); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ttk.OptionMenu(self, Pos7, *mid_pos, mid_pos[0]); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ttk.Label(self,text ='Midfielder 3',style="Label"); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ttk.OptionMenu(self, PL8, *Mid_names,Mid_names[0]); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ttk.OptionMenu(self, Pos8, *mid_pos, mid_pos[0]); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ttk.Label(self,text ='Midfielder 4',style="Label"); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ttk.OptionMenu(self, PL9, *Mid_names,Mid_names[0]); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ttk.OptionMenu(self, Pos9, *mid_pos, mid_pos[0]); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ttk.Label(self,text ='Attacker 1',style="Label"); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ttk.OptionMenu(self, PL10, *Att_names, Att_names[0]); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ttk.Label(self,text ='Position',style="Label"); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ttk.OptionMenu(self, Pos10, *att_pos, att_pos[0]); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ttk.Label(self,text ='Attacker 2',style="Label"); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ttk.OptionMenu(self, PL11, *Att_names,Att_names[0]); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ttk.OptionMenu(self, Pos11, *att_pos, att_pos[0]); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ttk.Label(self,text ='Sub GK',style="Label"); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ttk.OptionMenu(self, sub1, *GK_names, GK_names[0]); sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ttk.Label(self,text ='Sub 2',style="Label"); sub2_txt.grid(row=17,column=1)
        sub2_button = ttk.OptionMenu(self, sub2, *all_players, all_players[0]); sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ttk.Label(self,text ='Sub 3',style="Label"); sub3_txt.grid(row=18,column=1)
        sub3_button = ttk.OptionMenu(self, sub3, *all_players, all_players[0]); sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ttk.Label(self,text ='Sub 4',style="Label"); sub4_txt.grid(row=19,column=1)
        sub4_button = ttk.OptionMenu(self, sub4, *all_players, all_players[0]); sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ttk.Label(self,text ='Sub 5',style="Label"); sub5_txt.grid(row=20,column=1)
        sub5_button = ttk.OptionMenu(self, sub5, *all_players, all_players[0]); sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])

        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ttk.Label(self,text ='Def Tac 1',style="Label");  tac_txt1.grid(row=6,column=5)
        tac_btn1 = ttk.OptionMenu(self, tac1, *deff_tacs, deff_tacs[0]); tac1.set(tix[0]); tac_btn1.grid(row=6,column=6)
        #tac_btn2
        tac_txt2 = ttk.Label(self,text ='Def Tac 2',style="Label"); tac_txt2.grid(row=7,column=5)
        tac_btn2 = ttk.OptionMenu(self, tac2, *deff_tacs, deff_tacs[0]); tac2.set(tix[1]); tac_btn2.grid(row=7,column=6)
                #tac_btn2
        tac_txt3 = ttk.Label(self,text ='Mid Tac 1',style="Label"); tac_txt3.grid(row=8,column=5)
        tac_btn3 = ttk.OptionMenu(self, tac3, *mid_tacs, mid_tacs[0]); tac3.set(tix[2]); tac_btn3.grid(row=8,column=6)
                #tac_btn2
        tac_txt4 = ttk.Label(self,text ='Mid Tac 2',style="Label"); tac_txt4.grid(row=9,column=5)
        tac_btn4 = ttk.OptionMenu(self, tac4, *mid_tacs, mid_tacs[0]); tac4.set(tix[3]); tac_btn4.grid(row=9,column=6)
                #tac_btn2
        tac_txt5 = ttk.Label(self,text ='Att Tac 1',style="Label"); tac_txt5.grid(row=10,column=5)
        tac_btn5 = ttk.OptionMenu(self, tac5, *att_tacs, att_tacs[0]); tac5.set(tix[4]); tac_btn5.grid(row=10,column=6)
                #tac_btn2
        tac_txt6 = ttk.Label(self,text ='Att Tac 2',style="Label"); tac_txt6.grid(row=11,column=5)
        tac_btn6 = ttk.OptionMenu(self, tac6, *att_tacs, att_tacs[0]); tac6.set(tix[5]); tac_btn6.grid(row=11,column=6)
                #tac_btn2
        mstr_txt = ttk.Label(self,text ='Master',style="Label"); mstr_txt.grid(row=12,column=5)
        mstr_btn = ttk.OptionMenu(self, mstr, *master_tac, master_tac[0]); mstr.set(tix[6]); mstr_btn.grid(row=12,column=6)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ttk.Label(self,text ='Captain',style="Label"); cpt_txt.grid(row=14,column=5)
        cpt_btn = ttk.OptionMenu(self, cpt, *roles_list, roles_list[0]); cpt.set(rr[0]); cpt_btn.grid(row=14,column=6)
        
        frk_txt = ttk.Label(self,text ='Freekicks',style="Label"); frk_txt.grid(row=15,column=5)
        frk_btn = ttk.OptionMenu(self, frk, *roles_list, roles_list[0]); frk.set(rr[1]); frk_btn.grid(row=15,column=6)
        
        pen_txt = ttk.Label(self,text ='Penalties',style="Label"); pen_txt.grid(row=16,column=5)
        pen_btn = ttk.OptionMenu(self, pen, *roles_list, roles_list[0]); pen.set(rr[2]); pen_btn.grid(row=16,column=6) 

        
        # ================= CUP OPTIONS ================= #
        sub_opt1 = IntVar(); sub_opt2 = IntVar()
        Chck1_txt = ttk.Label(self,text ='Same team and tactics as league?',style="Label"); Chck1_txt.grid(row=18,column=8, columnspan=2)
        Chck1 = ttk.Checkbutton(self, text="", style="TCheckbutton", variable = sub_opt1, onvalue = 1, offvalue = 0); Chck1.grid(row=18,column=7)

        Chck2_txt = ttk.Label(self,text ='Same sub options as league?',style="Label"); Chck2_txt.grid(row=19,column=8, columnspan=2)
        Chck2 = ttk.Checkbutton(self, text="", style="TCheckbutton", variable = sub_opt2, onvalue = 1, offvalue = 0); Chck2.grid(row=19,column=7)

        
        # ================= TRAINING ================= #
        train1=StringVar();train2=StringVar();train3=StringVar();train4=StringVar();train5=StringVar();train6=StringVar();train7=StringVar();train8=StringVar();train9=StringVar();train10=StringVar()
        
        training_hours = []
        r1 = 0; r2 = 25
        while (r1<r2+1):
            training_hours.append(r1)
            r1+=1
            
        # get last week's submitted training
        train_prev = pd.read_excel(open(file2,"rb"), sheet_name="training")
        tp = train_prev.Training.tolist()
        
        #training btn 1
        tra_txt1 = ttk.Label(self,text ='Study Opp (L)',style="Label");  tra_txt1.grid(row=6,column=8, padx=(5,0))
        tra_btn1 = ttk.OptionMenu(self, train1, *training_hours, training_hours[0]); train1.set(tp[0]); tra_btn1.grid(row=6,column=9, padx=(2.5,0))
        #training btn 2
        tra_txt2 = ttk.Label(self,text ='Study Opp (C)',style="Label");  tra_txt2.grid(row=7,column=8, padx=(5,0))
        tra_btn2 = ttk.OptionMenu(self, train2, *training_hours, training_hours[0]); train2.set(tp[1]); tra_btn2.grid(row=7,column=9, padx=(2.5,0))
        #training btn 3
        tra_txt3 = ttk.Label(self,text ='Passing',style="Label");  tra_txt3.grid(row=8,column=8, padx=(5,0))
        tra_btn3 = ttk.OptionMenu(self, train3, *training_hours, training_hours[0]); train3.set(tp[2]); tra_btn3.grid(row=8,column=9, padx=(2.5,0))
        #training btn 4
        tra_txt4 = ttk.Label(self,text ='Ballskills',style="Label");  tra_txt4.grid(row=9,column=8, padx=(5,0))
        tra_btn4 = ttk.OptionMenu(self, train4, *training_hours, training_hours[0]); train4.set(tp[3]); tra_btn4.grid(row=9,column=9, padx=(2.5,0))
        #training btn 5
        tra_txt5 = ttk.Label(self,text ='Defensive',style="Label");  tra_txt5.grid(row=10,column=8, padx=(5,0))
        tra_btn5 = ttk.OptionMenu(self, train5, *training_hours, training_hours[0]); train5.set(tp[4]); tra_btn5.grid(row=10,column=9, padx=(2.5,0))
        #training btn 6
        tra_txt6 = ttk.Label(self,text ='Attacking',style="Label");  tra_txt6.grid(row=11,column=8, padx=(5,0))
        tra_btn6 = ttk.OptionMenu(self, train6, *training_hours, training_hours[0]); train6.set(tp[5]); tra_btn6.grid(row=11,column=9, padx=(2.5,0))
        #training btn 7
        tra_txt7 = ttk.Label(self,text ='Heading',style="Label");  tra_txt7.grid(row=12,column=8, padx=(5,0))
        tra_btn7 = ttk.OptionMenu(self, train7, *training_hours, training_hours[0]); train7.set(tp[6]); tra_btn7.grid(row=12,column=9, padx=(2.5,0))
        #training btn 8
        tra_txt8 = ttk.Label(self,text ='Five a sides',style="Label");  tra_txt8.grid(row=13,column=8, padx=(5,0))
        tra_btn8 = ttk.OptionMenu(self, train8, *training_hours, training_hours[0]); train8.set(tp[7]); tra_btn8.grid(row=13,column=9, padx=(2.5,0))
        #training btn 9
        tra_txt9 = ttk.Label(self,text ='Fitness',style="Label");  tra_txt9.grid(row=14,column=8, padx=(5,0))
        tra_btn9 = ttk.OptionMenu(self, train9, *training_hours, training_hours[0]); train9.set(tp[8]); tra_btn9.grid(row=14,column=9, padx=(2.5,0))
        #training btn 10
        tra_txt10 = ttk.Label(self,text ='Strength',style="Label");  tra_txt10.grid(row=15,column=8, padx=(5,0))
        tra_btn10 = ttk.OptionMenu(self, train10, *training_hours, training_hours[0]); train10.set(tp[9]); tra_btn10.grid(row=15,column=9, padx=(2.5,0))


        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar();name6=StringVar();name7=StringVar();name8=StringVar();name9=StringVar();name10=StringVar();
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar();action6=StringVar();action7=StringVar();action8=StringVar();action9=StringVar();action10=StringVar()
        actions = pd.read_csv("Actions/Actions.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0,"")
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.fillna("").Player.tolist()
        ap = actions_prev.fillna("").Action.tolist()

        #action btn 1
        act_txt1 = ttk.Label(self,text ='Name',style="Label");  act_txt1.grid(row=6,column=10,padx=5)
        act_btn1 = ttk.OptionMenu(self, name1, *roles_list, roles_list[0]); act_btn1.grid(row=6,column=11); name1.set(np[0]);
        lst_txt1 = ttk.Label(self,text ='Action',style="Label");  lst_txt1.grid(row=6,column=12,padx=2.5)
        list1 = ttk.OptionMenu(self, action1, *actions_list, actions_list[0]); action1.set(actions_list[0]); list1.grid(row=6,column=13); action1.set(ap[0])
        #action btn 2
        act_txt2 = ttk.Label(self,text ='Name',style="Label");  act_txt2.grid(row=7,column=10,padx=5)
        act_btn2 = ttk.OptionMenu(self, name2, *roles_list, roles_list[0]); act_btn2.grid(row=7,column=11); name2.set(np[1]);
        lst_txt2 = ttk.Label(self,text ='Action',style="Label");  lst_txt2.grid(row=7,column=12,padx=2.5)
        list2 = ttk.OptionMenu(self, action2, *actions_list, actions_list[0]); action2.set(actions_list[1]); list2.grid(row=7,column=13); action2.set(ap[1])
        #action btn 3
        act_txt3 = ttk.Label(self,text ='Name',style="Label");  act_txt3.grid(row=8,column=10,padx=5)
        act_btn3 = ttk.OptionMenu(self, name3, *roles_list, roles_list[0]); act_btn3.grid(row=8,column=11); name3.set(np[2]);
        lst_txt3 = ttk.Label(self,text ='Action',style="Label");  lst_txt3.grid(row=8,column=12,padx=2.5)
        list3 = ttk.OptionMenu(self, action3, *actions_list, actions_list[0]); action3.set(actions_list[2]); list3.grid(row=8,column=13); action3.set(ap[2])
        #action btn 4
        act_txt4 = ttk.Label(self,text ='Name',style="Label");  act_txt4.grid(row=9,column=10,padx=5)
        act_btn4 = ttk.OptionMenu(self, name4, *roles_list, roles_list[0]); act_btn4.grid(row=9,column=11); name4.set(np[3]);
        lst_txt4 = ttk.Label(self,text ='Action',style="Label");  lst_txt4.grid(row=9,column=12,padx=2.5)
        list4 = ttk.OptionMenu(self, action4, *actions_list, actions_list[0]); action4.set(actions_list[3]); list4.grid(row=9,column=13); action4.set(ap[3])
        #action btn 5
        act_txt5 = ttk.Label(self,text ='Name',style="Label");  act_txt5.grid(row=10,column=10,padx=5)
        act_btn5 = ttk.OptionMenu(self, name5, *roles_list, roles_list[0]); act_btn5.grid(row=10,column=11); name5.set(np[4]);
        lst_txt5 = ttk.Label(self,text ='Action',style="Label");  lst_txt5.grid(row=10,column=12,padx=2.5)
        list5 = ttk.OptionMenu(self, action5, *actions_list, actions_list[0]); action5.set(actions_list[4]); list5.grid(row=10,column=13); action5.set(ap[4])
        #action btn 6
        act_txt6 = ttk.Label(self,text ='Name',style="Label");  act_txt6.grid(row=11,column=10,padx=5)
        act_btn6 = ttk.OptionMenu(self, name6, *roles_list, roles_list[0]); act_btn6.grid(row=11,column=11); name6.set(np[5]);
        lst_txt6 = ttk.Label(self,text ='Action',style="Label");  lst_txt6.grid(row=11,column=12,padx=2.5)
        list6 = ttk.OptionMenu(self, action6, *actions_list, actions_list[0]); action6.set(actions_list[5]); list6.grid(row=11,column=13); action6.set(ap[5])
        #action btn 7
        act_txt7 = ttk.Label(self,text ='Name',style="Label");  act_txt7.grid(row=12,column=10,padx=5)
        act_btn7 = ttk.OptionMenu(self, name7, *roles_list, roles_list[0]); act_btn7.grid(row=12,column=11); name7.set(np[6]);
        lst_txt7 = ttk.Label(self,text ='Action',style="Label");  lst_txt7.grid(row=12,column=12,padx=2.5)
        list7 = ttk.OptionMenu(self, action7, *actions_list, actions_list[0]); action7.set(actions_list[6]); list7.grid(row=12,column=13); action7.set(ap[6])
        #action btn 8
        act_txt8 = ttk.Label(self,text ='Name',style="Label");  act_txt8.grid(row=13,column=10,padx=5)
        act_btn8 = ttk.OptionMenu(self, name8, *roles_list, roles_list[0]); act_btn8.grid(row=13,column=11); name8.set(np[7]);
        lst_txt8 = ttk.Label(self,text ='Action',style="Label");  lst_txt8.grid(row=13,column=12,padx=2.5)
        list8 = ttk.OptionMenu(self, action8, *actions_list, actions_list[0]); action8.set(actions_list[7]); list8.grid(row=13,column=13); action8.set(ap[7])
        #action btn 9
        act_txt9 = ttk.Label(self,text ='Name',style="Label");  act_txt9.grid(row=14,column=10,padx=5)
        act_btn9 = ttk.OptionMenu(self, name9, *roles_list, roles_list[0]); act_btn9.grid(row=14,column=11); name9.set(np[8]);
        lst_txt9 = ttk.Label(self,text ='Action',style="Label");  lst_txt9.grid(row=14,column=12,padx=2.5)
        list9 = ttk.OptionMenu(self, action9, *actions_list, actions_list[0]); action9.set(actions_list[8]); list9.grid(row=14,column=13); action9.set(ap[8])
        #action btn 10
        act_txt10 = ttk.Label(self,text ='Name',style="Label");  act_txt10.grid(row=15,column=10,padx=5)
        act_btn10 = ttk.OptionMenu(self, name10, *roles_list, roles_list[0]); act_btn10.grid(row=15,column=11); name10.set(np[9]);
        lst_txt10 = ttk.Label(self,text ='Action',style="Label");  lst_txt10.grid(row=15,column=12,padx=2.5)
        list10 = ttk.OptionMenu(self, action10, *actions_list, actions_list[0]); action10.set(actions_list[9]); list10.grid(row=15,column=13); action10.set(ap[9])

        # ================= MESSAGE ================= #
        message = StringVar()
        message_txt = ttk.Label(self,text ='Message',style="Label")
        message_txt.grid(row=21,column=7,pady=(4,0))
        message_input = ttk.Entry(self, textvariable=message)
        message_input.grid(row=21,column=8,pady=(4,0))

        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ttk.Label(self,text ='Password',style="Label")
        passwd_txt.grid(row=22,column=7,pady=(4,0))
        passwd_input = ttk.Entry(self, textvariable=passwd)
        passwd_input.grid(row=22,column=8,pady=(4,0))

        
        # ================= FORMATIONS ================= #
        Formation_txt = ttk.Label(self,text="Formation: ",style="Label").grid(row=2, column=6, padx=(10,0))
        global formation
        formation = 442
        
        def five_four_one(self):
            global formation; formation = 541
            
            PL6_menu = PL6_button['menu']
            PL6_menu.delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_menu.add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")

            PL10_menu = PL10_button['menu']
            PL10_menu.delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_menu.add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Midfielder 4")
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="disabled") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 541 button
        form_541 = ttk.Button(self, text="541", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))


            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")

            form_541.config(state="normal") # Disable the button
            form_532.config(state="disabled") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 532 button
        form_532 = ttk.Button(self, text="532", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")

            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="disabled") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 442 button
        form_442 = ttk.Button(self, text="442", state="disabled", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation; formation = 451; print(formation)

            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))
            
            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")
            P10_txt.config(text="Midfielder 5")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="disabled") # Disable the button
            
        # 442 button
        form_451 = ttk.Button(self, text="451", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10, padx=(2,0))
        
        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_first_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.ticks = (sub_opt1.get(),sub_opt2.get())
            self.training = (train1.get(),train2.get(),train3.get(),train4.get(),train5.get(),train6.get(),train7.get(),train8.get(),train9.get(),train10.get())
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get(),name6.get(),name7.get(),name8.get(),name9.get(),name10.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get(),action6.get(),action7.get(),action8.get(),action9.get(),action10.get())
            self.submit_button.config(state="normal")
            self.password = passwd.get()
            self.message = message.get()
            print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}")
            print(f'Password entered is "{self.password}"')

        # set button
        set_btn = ttk.Button(self, text="Set First Team", command=lambda: set_first_team(self)) # set button
        set_btn.grid(row=2, column=4,pady=10, padx=10)
        
        # ================= SUBMIT ================= #
        self.submit_button = ttk.Button(self, text="Submit", command=lambda: self.controller.submit_first_team(self.players,self.positions,self.tactics,self.roles,self.roles_df,self.ticks,self.training,self.actions,self.names,self.password,formation,self.message))
        self.submit_button.config(state=DISABLED)
        self.submit_button.grid(row=2, column=3,pady=10, padx=10)

        
# =================================== FIRST TEAM ====================================== #


# #### Reserves Class

# In[16]:


# =================================== RESERVES ====================================== #

class Reserves(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.config(bg="lightblue")


        # ============== STYLE =============== #
        
        # This will create style object
        style = ttk.Style()
        
        # Label style
        style.configure('Label', font = ('calibri', 10), foreground = 'black', background = "lightblue")

        # Title
        title = ttk.Label(self, text="Reserve Team", style='Label')
        title.grid(row=1, column=1,pady=10, padx=10)
        
        # reserve button
        button1 = ttk.Button(self, text="First Team", command=lambda: controller.show_frame(First))
        button1.grid(row=2, column=1,pady=10, padx=10)

        # youth button
        button2 = ttk.Button(self, text="Youths", command=lambda: controller.show_frame(Youths))
        button2.grid(row=2, column=2,pady=10, padx=10)

        # set filepaths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Res Sub.xlsx"
        # get pd dfs
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file,"rb"), sheet_name="r_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="r_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="r_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="r_att")
        DFA = pd.concat([deff,mid,att])

       # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only


        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist();
        Deff_names = deff['Name'].tolist(); 
        Mid_names = mid['Name'].tolist(); 
        Att_names = att['Name'].tolist(); 
        all_players = GK_names + Deff_names + Mid_names + Att_names
        
        # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar(); PL3 = StringVar(); PL4 = StringVar(); PL5 = StringVar(); PL6 = StringVar(); PL7 = StringVar(); PL8 = StringVar(); PL9 = StringVar(); PL10 = StringVar(); PL11 = StringVar() # store player names
        Pos2 = StringVar(); Pos3 = StringVar(); Pos4 = StringVar(); Pos5 = StringVar(); Pos6 = StringVar(); Pos7 = StringVar(); Pos8 = StringVar(); Pos9 = StringVar();Pos10 = StringVar(); Pos11 = StringVar()  # store positions
        sub1 = StringVar(); sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar(); # store sub names
        
        #------------- GK drop downs --------------#
        GK_txt = ttk.Label(self,text ='Goalkeeper',style="Label"); GK_txt.grid(row=5, column=1,pady=(10,0), padx=0)
        PL1_btn = ttk.OptionMenu(self, PL1, *GK_names, GK_names[0]); PL1.set(GK_names[0]);PL1_btn.grid(row=5, column=2,pady=(10,0), padx=0) # button to choose GK
        
        #------------- Defender drop downs --------------#
        P2_txt = ttk.Label(self,text ='Defender 1',style="Label"); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ttk.OptionMenu(self, PL2, *Deff_names,Deff_names[0]); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ttk.Label(self,text ='Position',style="Label"); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ttk.OptionMenu(self, Pos2, *deff_pos, deff_pos[0]); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ttk.Label(self,text ='Defender 2',style="Label"); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ttk.OptionMenu(self, PL3, *Deff_names,Deff_names[0]); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ttk.OptionMenu(self, Pos3, *deff_pos, deff_pos[0]); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ttk.Label(self,text ='Defender 3',style="Label"); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ttk.OptionMenu(self, PL4, *Deff_names,Deff_names[0]); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ttk.OptionMenu(self, Pos4, *deff_pos, deff_pos[0]); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ttk.Label(self,text ='Defender 4',style="Label"); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ttk.OptionMenu(self, PL5, *Deff_names,Deff_names[0]); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ttk.OptionMenu(self, Pos5, *deff_pos, deff_pos[0]); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ttk.Label(self,text ='Midfielder 1',style="Label"); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ttk.OptionMenu(self, PL6, *Mid_names,Mid_names[0]); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ttk.Label(self,text ='Position',style="Label"); Pos6_txt.grid(row=10,column=3,pady=(10,0))
        PL6_pos = ttk.OptionMenu(self, Pos6, *mid_pos, mid_pos[0]); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ttk.Label(self,text ='Midfielder 2',style="Label"); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ttk.OptionMenu(self, PL7, *Mid_names,Mid_names[0]); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ttk.OptionMenu(self, Pos7, *mid_pos, mid_pos[0]); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ttk.Label(self,text ='Midfielder 3',style="Label"); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ttk.OptionMenu(self, PL8, *Mid_names,Mid_names[0]); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ttk.OptionMenu(self, Pos8, *mid_pos, mid_pos[0]); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ttk.Label(self,text ='Midfielder 4',style="Label"); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ttk.OptionMenu(self, PL9, *Mid_names,Mid_names[0]); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ttk.OptionMenu(self, Pos9, *mid_pos, mid_pos[0]); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ttk.Label(self,text ='Attacker 1',style="Label"); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ttk.OptionMenu(self, PL10, *Att_names, Att_names[0]); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ttk.Label(self,text ='Position',style="Label"); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ttk.OptionMenu(self, Pos10, *att_pos, att_pos[0]); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ttk.Label(self,text ='Attacker 2',style="Label"); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ttk.OptionMenu(self, PL11, *Att_names,Att_names[0]); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ttk.OptionMenu(self, Pos11, *att_pos, att_pos[0]); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ttk.Label(self,text ='Sub GK',style="Label"); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ttk.OptionMenu(self, sub1, *GK_names, GK_names[0]); sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ttk.Label(self,text ='Sub 2',style="Label"); sub2_txt.grid(row=17,column=1)
        sub2_button = ttk.OptionMenu(self, sub2, *all_players, all_players[0]); sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ttk.Label(self,text ='Sub 3',style="Label"); sub3_txt.grid(row=18,column=1)
        sub3_button = ttk.OptionMenu(self, sub3, *all_players, all_players[0]); sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ttk.Label(self,text ='Sub 4',style="Label"); sub4_txt.grid(row=19,column=1)
        sub4_button = ttk.OptionMenu(self, sub4, *all_players, all_players[0]); sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ttk.Label(self,text ='Sub 5',style="Label"); sub5_txt.grid(row=20,column=1)
        sub5_button = ttk.OptionMenu(self, sub5, *all_players, all_players[0]); sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])
        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ttk.Label(self,text ='Def Tac 1',style="Label");  tac_txt1.grid(row=6,column=7)
        tac_btn1 = ttk.OptionMenu(self, tac1, *deff_tacs, deff_tacs[0]); tac1.set(tix[0]); tac_btn1.grid(row=6,column=8)
        #tac_btn2
        tac_txt2 = ttk.Label(self,text ='Def Tac 2',style="Label"); tac_txt2.grid(row=7,column=7)
        tac_btn2 = ttk.OptionMenu(self, tac2, *deff_tacs, deff_tacs[0]); tac2.set(tix[1]); tac_btn2.grid(row=7,column=8)
                #tac_btn2
        tac_txt3 = ttk.Label(self,text ='Mid Tac 1',style="Label"); tac_txt3.grid(row=8,column=7)
        tac_btn3 = ttk.OptionMenu(self, tac3, *mid_tacs, mid_tacs[0]); tac3.set(tix[2]); tac_btn3.grid(row=8,column=8)
                #tac_btn2
        tac_txt4 = ttk.Label(self,text ='Mid Tac 2',style="Label"); tac_txt4.grid(row=9,column=7)
        tac_btn4 = ttk.OptionMenu(self, tac4, *mid_tacs, mid_tacs[0]); tac4.set(tix[3]); tac_btn4.grid(row=9,column=8)
                #tac_btn2
        tac_txt5 = ttk.Label(self,text ='Att Tac 1',style="Label"); tac_txt5.grid(row=10,column=7)
        tac_btn5 = ttk.OptionMenu(self, tac5, *att_tacs, att_tacs[0]); tac5.set(tix[4]); tac_btn5.grid(row=10,column=8)
                #tac_btn2
        tac_txt6 = ttk.Label(self,text ='Att Tac 2',style="Label"); tac_txt6.grid(row=11,column=7)
        tac_btn6 = ttk.OptionMenu(self, tac6, *att_tacs, att_tacs[0]); tac6.set(tix[5]); tac_btn6.grid(row=11,column=8)
                #tac_btn2
        mstr_txt = ttk.Label(self,text ='Master',style="Label"); mstr_txt.grid(row=12,column=7)
        mstr_btn = ttk.OptionMenu(self, mstr, *master_tac, master_tac[0]); mstr.set(tix[6]); mstr_btn.grid(row=12,column=8)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ttk.Label(self,text ='Captain',style="Label"); cpt_txt.grid(row=14,column=7)
        cpt_btn = ttk.OptionMenu(self, cpt, *roles_list, roles_list[0]); cpt.set(rr[0]); cpt_btn.grid(row=14,column=8)
        
        frk_txt = ttk.Label(self,text ='Freekicks',style="Label"); frk_txt.grid(row=15,column=7)
        frk_btn = ttk.OptionMenu(self, frk, *roles_list, roles_list[0]); frk.set(rr[1]); frk_btn.grid(row=15,column=8)
        
        pen_txt = ttk.Label(self,text ='Penalties',style="Label"); pen_txt.grid(row=16,column=7)
        pen_btn = ttk.OptionMenu(self, pen, *roles_list, roles_list[0]); pen.set(rr[2]); pen_btn.grid(row=16,column=8) 

        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar()
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar()
        actions = pd.read_csv("Actions/Actions.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0,"")
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.Player.fillna("").tolist()
        ap = actions_prev.Action.fillna("").tolist()

        #action btn 1
        act_txt1 = ttk.Label(self,text ='Name',style="Label");  act_txt1.grid(row=6,column=9,padx=2.5)
        act_btn1 = ttk.OptionMenu(self, name1, *roles_list, roles_list[0]); act_btn1.grid(row=6,column=10); name1.set(np[0]);
        lst_txt1 = ttk.Label(self,text ='Action',style="Label");  lst_txt1.grid(row=6,column=11,padx=2.5)
        list1 = ttk.OptionMenu(self, action1, *actions_list, actions_list[0]); action1.set(actions_list[0]); list1.grid(row=6,column=12); action1.set(ap[0])
        #action btn 2
        act_txt2 = ttk.Label(self,text ='Name',style="Label");  act_txt2.grid(row=7,column=9,padx=2.5)
        act_btn2 = ttk.OptionMenu(self, name2, *roles_list, roles_list[0]); act_btn2.grid(row=7,column=10); name2.set(np[1]);
        lst_txt2 = ttk.Label(self,text ='Action',style="Label");  lst_txt2.grid(row=7,column=11,padx=2.5)
        list2 = ttk.OptionMenu(self, action2, *actions_list, actions_list[0]); action2.set(actions_list[1]); list2.grid(row=7,column=12); action2.set(ap[1])
        #action btn 3
        act_txt3 = ttk.Label(self,text ='Name',style="Label");  act_txt3.grid(row=8,column=9,padx=2.5)
        act_btn3 = ttk.OptionMenu(self, name3, *roles_list, roles_list[0]); act_btn3.grid(row=8,column=10); name3.set(np[2]);
        lst_txt3 = ttk.Label(self,text ='Action',style="Label");  lst_txt3.grid(row=8,column=11,padx=2.5)
        list3 = ttk.OptionMenu(self, action3, *actions_list, actions_list[0]); action3.set(actions_list[2]); list3.grid(row=8,column=12); action3.set(ap[2])
        #action btn 4
        act_txt4 = ttk.Label(self,text ='Name',style="Label");  act_txt4.grid(row=9,column=9,padx=2.5)
        act_btn4 = ttk.OptionMenu(self, name4, *roles_list, roles_list[0]); act_btn4.grid(row=9,column=10); name4.set(np[3]);
        lst_txt4 = ttk.Label(self,text ='Action',style="Label");  lst_txt4.grid(row=9,column=11,padx=2.5)
        list4 = ttk.OptionMenu(self, action4, *actions_list, actions_list[0]); action4.set(actions_list[3]); list4.grid(row=9,column=12); action4.set(ap[3])
        #action btn 5
        act_txt5 = ttk.Label(self,text ='Name',style="Label");  act_txt5.grid(row=10,column=9,padx=2.5)
        act_btn5 = ttk.OptionMenu(self, name5, *roles_list, roles_list[0]); act_btn5.grid(row=10,column=10); name5.set(np[4]);
        lst_txt5 = ttk.Label(self,text ='Action',style="Label");  lst_txt5.grid(row=10,column=11,padx=2.5)
        list5 = ttk.OptionMenu(self, action5, *actions_list, actions_list[0]); action5.set(actions_list[4]); list5.grid(row=10,column=12); action5.set(ap[4])

        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ttk.Label(self,text ='Password',style="Label").grid(row=21,column=7,pady=(50,0))
        passwd_input = ttk.Entry(self, textvariable=passwd).grid(row=21,column=8,columnspan=4,pady=(50,0))

        
        # ================= FORMATIONS ================= #
        Formation_txt = ttk.Label(self,text="Formation: ",style="Label").grid(row=2, column=6, padx=(10,0))
        global formation
        formation = 442
        
        def five_four_one(self):
            global formation; formation = 541
            
            PL6_menu = PL6_button['menu']
            PL6_menu.delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_menu.add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")

            PL10_menu = PL10_button['menu']
            PL10_menu.delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_menu.add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Midfielder 4")
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="disabled") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 541 button
        form_541 = ttk.Button(self, text="541", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))


            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")

            form_541.config(state="normal") # Disable the button
            form_532.config(state="disabled") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 532 button
        form_532 = ttk.Button(self, text="532", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")

            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="disabled") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 442 button
        form_442 = ttk.Button(self, text="442", state="disabled", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation; formation = 451; print(formation)

            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))
            
            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")
            P10_txt.config(text="Midfielder 5")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="disabled") # Disable the button
            
        # 442 button
        form_451 = ttk.Button(self, text="451", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10, padx=(2,0))

        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_res_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get())
            self.password = passwd.get()
            self.submit_button.config(state="normal")
            
            print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}")
            print(f'Password entered is "{self.password}"')
            
        
        # set button
        set_btn = ttk.Button(self, text="Set Reserve Team", command=lambda: set_res_team(self)).grid(row=2, column=4,pady=10, padx=10) # set button

        # ================= SUBMIT ================= #
        self.submit_button = ttk.Button(self, text="Submit", command=lambda: self.controller.submit_res_team(self.players,self.positions,self.tactics,self.roles,self.roles_df,self.actions,self.names,self.password,formation))
        self.submit_button.config(state=DISABLED)
        self.submit_button.grid(row=2, column=3,pady=10, padx=10)


# #### Youths Class

# In[17]:


# =================================== YOUTHS ====================================== #

class Youths(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="lightblue")


        # ============== STYLE =============== #
        
        # This will create style object
        style = ttk.Style()
        
        # Label style
        style.configure('Title', font = ('calibri', 14), foreground = 'black', background = "lightblue")
        
        # Label style
        style.configure('Label', font = ('calibri', 10), foreground = 'black', background = "lightblue")

        # Title
        title = ttk.Label(self, text="Youths", style='Label')
        title.grid(row=1, column=1,pady=10, padx=10)
        
        # reserve button
        button1 = ttk.Button(self, text="First Team", command=lambda: controller.show_frame(First))
        button1.grid(row=2, column=1,pady=10, padx=10)

        # youth button
        button2 = ttk.Button(self, text="Reserves", command=lambda: controller.show_frame(Reserves))
        button2.grid(row=2, column=2,pady=10, padx=10)

        # set filepaths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Yth Sub.xlsx"
        # get pd dfs
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file,"rb"), sheet_name="y_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="y_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="y_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="y_att")
        DFA = pd.concat([deff,mid,att])

       # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only


        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist();
        Deff_names = deff['Name'].tolist(); 
        Mid_names = mid['Name'].tolist(); 
        Att_names = att['Name'].tolist(); 
        all_players = GK_names + Deff_names + Mid_names + Att_names
        
        # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar(); PL3 = StringVar(); PL4 = StringVar(); PL5 = StringVar(); PL6 = StringVar(); PL7 = StringVar(); PL8 = StringVar(); PL9 = StringVar(); PL10 = StringVar(); PL11 = StringVar() # store player names
        Pos2 = StringVar(); Pos3 = StringVar(); Pos4 = StringVar(); Pos5 = StringVar(); Pos6 = StringVar(); Pos7 = StringVar(); Pos8 = StringVar(); Pos9 = StringVar();Pos10 = StringVar(); Pos11 = StringVar()  # store positions
        sub1 = StringVar(); sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar(); # store sub names
        
        #------------- GK drop downs --------------#
        GK_txt = ttk.Label(self,text ='Goalkeeper',style="Label"); GK_txt.grid(row=5, column=1,pady=(10,0), padx=0)
        PL1_btn = ttk.OptionMenu(self, PL1, *GK_names, GK_names[0]); PL1.set(GK_names[0]);PL1_btn.grid(row=5, column=2,pady=(10,0), padx=0) # button to choose GK
        
        #------------- Defender drop downs --------------#
        P2_txt = ttk.Label(self,text ='Defender 1',style="Label"); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ttk.OptionMenu(self, PL2, *Deff_names,Deff_names[0]); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ttk.Label(self,text ='Position',style="Label"); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ttk.OptionMenu(self, Pos2, *deff_pos, deff_pos[0]); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ttk.Label(self,text ='Defender 2',style="Label"); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ttk.OptionMenu(self, PL3, *Deff_names,Deff_names[0]); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ttk.OptionMenu(self, Pos3, *deff_pos, deff_pos[0]); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ttk.Label(self,text ='Defender 3',style="Label"); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ttk.OptionMenu(self, PL4, *Deff_names,Deff_names[0]); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ttk.OptionMenu(self, Pos4, *deff_pos, deff_pos[0]); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ttk.Label(self,text ='Defender 4',style="Label"); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ttk.OptionMenu(self, PL5, *Deff_names,Deff_names[0]); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ttk.OptionMenu(self, Pos5, *deff_pos, deff_pos[0]); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ttk.Label(self,text ='Midfielder 1',style="Label"); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ttk.OptionMenu(self, PL6, *Mid_names,Mid_names[0]); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ttk.Label(self,text ='Position',style="Label"); Pos6_txt.grid(row=10,column=3,pady=(10,0))
        PL6_pos = ttk.OptionMenu(self, Pos6, *mid_pos, mid_pos[0]); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ttk.Label(self,text ='Midfielder 2',style="Label"); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ttk.OptionMenu(self, PL7, *Mid_names,Mid_names[0]); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ttk.OptionMenu(self, Pos7, *mid_pos, mid_pos[0]); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ttk.Label(self,text ='Midfielder 3',style="Label"); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ttk.OptionMenu(self, PL8, *Mid_names,Mid_names[0]); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ttk.OptionMenu(self, Pos8, *mid_pos, mid_pos[0]); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ttk.Label(self,text ='Midfielder 4',style="Label"); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ttk.OptionMenu(self, PL9, *Mid_names,Mid_names[0]); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ttk.OptionMenu(self, Pos9, *mid_pos, mid_pos[0]); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ttk.Label(self,text ='Attacker 1',style="Label"); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ttk.OptionMenu(self, PL10, *Att_names, Att_names[0]); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ttk.Label(self,text ='Position',style="Label"); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ttk.OptionMenu(self, Pos10, *att_pos, att_pos[0]); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ttk.Label(self,text ='Attacker 2',style="Label"); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ttk.OptionMenu(self, PL11, *Att_names,Att_names[0]); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ttk.OptionMenu(self, Pos11, *att_pos, att_pos[0]); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ttk.Label(self,text ='Sub GK',style="Label"); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ttk.OptionMenu(self, sub1, *GK_names, GK_names[0]); sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ttk.Label(self,text ='Sub 2',style="Label"); sub2_txt.grid(row=17,column=1)
        sub2_button = ttk.OptionMenu(self, sub2, *all_players, all_players[0]); sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ttk.Label(self,text ='Sub 3',style="Label"); sub3_txt.grid(row=18,column=1)
        sub3_button = ttk.OptionMenu(self, sub3, *all_players, all_players[0]); sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ttk.Label(self,text ='Sub 4',style="Label"); sub4_txt.grid(row=19,column=1)
        sub4_button = ttk.OptionMenu(self, sub4, *all_players, all_players[0]); sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ttk.Label(self,text ='Sub 5',style="Label"); sub5_txt.grid(row=20,column=1)
        sub5_button = ttk.OptionMenu(self, sub5, *all_players, all_players[0]); sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])

        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ttk.Label(self,text ='Def Tac 1',style="Label");  tac_txt1.grid(row=6,column=7)
        tac_btn1 = ttk.OptionMenu(self, tac1, *deff_tacs, deff_tacs[0]); tac1.set(tix[0]); tac_btn1.grid(row=6,column=8)
        #tac_btn2
        tac_txt2 = ttk.Label(self,text ='Def Tac 2',style="Label"); tac_txt2.grid(row=7,column=7)
        tac_btn2 = ttk.OptionMenu(self, tac2, *deff_tacs, deff_tacs[0]); tac2.set(tix[1]); tac_btn2.grid(row=7,column=8)
                #tac_btn2
        tac_txt3 = ttk.Label(self,text ='Mid Tac 1',style="Label"); tac_txt3.grid(row=8,column=7)
        tac_btn3 = ttk.OptionMenu(self, tac3, *mid_tacs, mid_tacs[0]); tac3.set(tix[2]); tac_btn3.grid(row=8,column=8)
                #tac_btn2
        tac_txt4 = ttk.Label(self,text ='Mid Tac 2',style="Label"); tac_txt4.grid(row=9,column=7)
        tac_btn4 = ttk.OptionMenu(self, tac4, *mid_tacs, mid_tacs[0]); tac4.set(tix[3]); tac_btn4.grid(row=9,column=8)
                #tac_btn2
        tac_txt5 = ttk.Label(self,text ='Att Tac 1',style="Label"); tac_txt5.grid(row=10,column=7)
        tac_btn5 = ttk.OptionMenu(self, tac5, *att_tacs, att_tacs[0]); tac5.set(tix[4]); tac_btn5.grid(row=10,column=8)
                #tac_btn2
        tac_txt6 = ttk.Label(self,text ='Att Tac 2',style="Label"); tac_txt6.grid(row=11,column=7)
        tac_btn6 = ttk.OptionMenu(self, tac6, *att_tacs, att_tacs[0]); tac6.set(tix[5]); tac_btn6.grid(row=11,column=8)
                #tac_btn2
        mstr_txt = ttk.Label(self,text ='Master',style="Label"); mstr_txt.grid(row=12,column=7)
        mstr_btn = ttk.OptionMenu(self, mstr, *master_tac, master_tac[0]); mstr.set(tix[6]); mstr_btn.grid(row=12,column=8)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ttk.Label(self,text ='Captain',style="Label"); cpt_txt.grid(row=14,column=7)
        cpt_btn = ttk.OptionMenu(self, cpt, *roles_list, roles_list[0]); cpt.set(rr[0]); cpt_btn.grid(row=14,column=8)
        
        frk_txt = ttk.Label(self,text ='Freekicks',style="Label"); frk_txt.grid(row=15,column=7)
        frk_btn = ttk.OptionMenu(self, frk, *roles_list, roles_list[0]); frk.set(rr[1]); frk_btn.grid(row=15,column=8)
        
        pen_txt = ttk.Label(self,text ='Penalties',style="Label"); pen_txt.grid(row=16,column=7)
        pen_btn = ttk.OptionMenu(self, pen, *roles_list, roles_list[0]); pen.set(rr[2]); pen_btn.grid(row=16,column=8) 

        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar()
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar()
        actions = pd.read_csv("Actions/Actions.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0,"")
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.Player.fillna("").tolist()
        ap = actions_prev.Action.fillna("").tolist()

        #action btn 1
        act_txt1 = ttk.Label(self,text ='Name',style="Label");  act_txt1.grid(row=6,column=9,padx=2.5)
        act_btn1 = ttk.OptionMenu(self, name1, *roles_list, roles_list[0]); act_btn1.grid(row=6,column=10); name1.set(np[0]);
        lst_txt1 = ttk.Label(self,text ='Action',style="Label");  lst_txt1.grid(row=6,column=11,padx=2.5)
        list1 = ttk.OptionMenu(self, action1, *actions_list, actions_list[0]); action1.set(actions_list[0]); list1.grid(row=6,column=12); action1.set(ap[0])
        #action btn 2
        act_txt2 = ttk.Label(self,text ='Name',style="Label");  act_txt2.grid(row=7,column=9,padx=2.5)
        act_btn2 = ttk.OptionMenu(self, name2, *roles_list, roles_list[0]); act_btn2.grid(row=7,column=10); name2.set(np[1]);
        lst_txt2 = ttk.Label(self,text ='Action',style="Label");  lst_txt2.grid(row=7,column=11,padx=2.5)
        list2 = ttk.OptionMenu(self, action2, *actions_list, actions_list[0]); action2.set(actions_list[1]); list2.grid(row=7,column=12); action2.set(ap[1])
        #action btn 3
        act_txt3 = ttk.Label(self,text ='Name',style="Label");  act_txt3.grid(row=8,column=9,padx=2.5)
        act_btn3 = ttk.OptionMenu(self, name3, *roles_list, roles_list[0]); act_btn3.grid(row=8,column=10); name3.set(np[2]);
        lst_txt3 = ttk.Label(self,text ='Action',style="Label");  lst_txt3.grid(row=8,column=11,padx=2.5)
        list3 = ttk.OptionMenu(self, action3, *actions_list, actions_list[0]); action3.set(actions_list[2]); list3.grid(row=8,column=12); action3.set(ap[2])
        #action btn 4
        act_txt4 = ttk.Label(self,text ='Name',style="Label");  act_txt4.grid(row=9,column=9,padx=2.5)
        act_btn4 = ttk.OptionMenu(self, name4, *roles_list, roles_list[0]); act_btn4.grid(row=9,column=10); name4.set(np[3]);
        lst_txt4 = ttk.Label(self,text ='Action',style="Label");  lst_txt4.grid(row=9,column=11,padx=2.5)
        list4 = ttk.OptionMenu(self, action4, *actions_list, actions_list[0]); action4.set(actions_list[3]); list4.grid(row=9,column=12); action4.set(ap[3])
        #action btn 5
        act_txt5 = ttk.Label(self,text ='Name',style="Label");  act_txt5.grid(row=10,column=9,padx=2.5)
        act_btn5 = ttk.OptionMenu(self, name5, *roles_list, roles_list[0]); act_btn5.grid(row=10,column=10); name5.set(np[4]);
        lst_txt5 = ttk.Label(self,text ='Action',style="Label");  lst_txt5.grid(row=10,column=11,padx=2.5)
        list5 = ttk.OptionMenu(self, action5, *actions_list, actions_list[0]); action5.set(actions_list[4]); list5.grid(row=10,column=12); action5.set(ap[4])

        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ttk.Label(self,text ='Password',style="Label").grid(row=21,column=7,pady=(50,0))
        passwd_input = ttk.Entry(self, textvariable=passwd).grid(row=21,column=8,columnspan=4,pady=(50,0))

        
        # ================= FORMATIONS ================= #
        Formation_txt = ttk.Label(self,text="Formation: ",style="Label").grid(row=2, column=6, padx=(10,0))
        global formation
        formation = 442
        
        def five_four_one(self):
            global formation; formation = 541
            
            PL6_menu = PL6_button['menu']
            PL6_menu.delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_menu.add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")

            PL10_menu = PL10_button['menu']
            PL10_menu.delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_menu.add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Midfielder 4")
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="disabled") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 541 button
        form_541 = ttk.Button(self, text="541", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Deff_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))

            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in deff_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))


            P6_txt.config(text="Defender 5") # Update label
            P7_txt.config(text="Midfielder 1")
            P8_txt.config(text="Midfielder 2")
            P9_txt.config(text="Midfielder 3")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")

            form_541.config(state="normal") # Disable the button
            form_532.config(state="disabled") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 532 button
        form_532 = ttk.Button(self, text="532", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442
            
            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in att_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))

            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")

            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Att_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P10_txt.config(text="Attacker 1")
            P11_txt.config(text="Attacker 2")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="disabled") # Disable the button
            form_451.config(state="normal") # Disable the button
            
        # 442 button
        form_442 = ttk.Button(self, text="442", state="disabled", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation; formation = 451; print(formation)

            PL6_button['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in Mid_names:
                PL6_button['menu'].add_command(label=name, command=tk._setit(PL6, name))
            
            PL6_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL6_pos['menu'].add_command(label=name, command=tk._setit(Pos6, name))
            
            PL10_pos['menu'].delete(0, 'end') # Clear current options # Update PL6 with mid_names
            for name in mid_pos:
                PL10_pos['menu'].add_command(label=name, command=tk._setit(Pos10, name))
            
            P6_txt.config(text="Midfielder 1") # Update label
            P7_txt.config(text="Midfielder 2")
            P8_txt.config(text="Midfielder 3")
            P9_txt.config(text="Midfielder 4")
            P10_txt.config(text="Midfielder 5")
            
            PL10_button['menu'].delete(0, 'end') # Clear current options  # Update options menu with new options
            for name in Mid_names:
                PL10_button['menu'].add_command(label=name, command=tk._setit(PL10, name))
                
            P11_txt.config(text="Attacker 1")
            
            form_541.config(state="normal") # Disable the button
            form_532.config(state="normal") # Disable the button
            form_442.config(state="normal") # Disable the button
            form_451.config(state="disabled") # Disable the button
            
        # 442 button
        form_451 = ttk.Button(self, text="451", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10, padx=(2,0))

        
        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_youth_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get())
            self.password = passwd.get()
            self.submit_button.config(state="normal")
            
            print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}")
            print(f'Password entered is "{self.password}"')
            
        
        # set button
        set_btn = ttk.Button(self, text="Set Youth Team", command=lambda: set_youth_team(self)).grid(row=2, column=4,pady=10, padx=10) # set button

        # ================= SUBMIT ================= #
        self.submit_button = ttk.Button(self, text="Submit", command=lambda: self.controller.submit_yth_team(self.players,self.positions,self.tactics,self.roles,self.roles_df,self.actions,self.names,self.password,formation))
        self.submit_button.config(state=DISABLED)
        self.submit_button.grid(row=2, column=3,pady=10, padx=10)


# #### Execute

# In[18]:


if __name__ == "__main__":
    app = UEApp()
    app.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:




