#!/usr/bin/env python
# coding: utf-8

# # Imports and Options

# #### Installation Instructions

# How to install:
# - Download Python for Windows 64 bit
# - Download the latest Java for Windows 64bit
# - Firefox driver
# - Hit "Win + R" to open cmd.
# - Type: "py -m pip install jupyter lab jpype1 tabula-py PyPDF2 Selenium tk ttkthemes pandatables"
# 

# #### Imports for MDS Data Extraction

# In[1]:


import PyPDF2
from PyPDF2 import PdfReader
import re
import pandas as pd
import tabula
import numpy as np 
import warnings
import time


# Set Pandas Options

# In[2]:


pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'
warnings.simplefilter(action='ignore', category=FutureWarning)


# # Get Stuff

# #### Get PDF

# Open a window and browse for the pdf file

# In[3]:


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from os import name as os_name
import os
from os import getlogin

class Feedback:         
    def __init__(self, master):

    
        def Close(): 
            master.destroy() 
            
        # frame_content
        self.frame_header = ttk.Frame(master)
        
        self.frame_header.grid(row=1,column=0,sticky="nsew")
        master.configure(background = '#0065a3')
        master.geometry("450x250")
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#0065a3')
        self.style.configure('TButton', background = '#006da3')
        self.style.configure('TLabel', background = '#0065a3')

        # frame2
        self.frame2 = ttk.Frame(master)
        self.frame2.grid(row=0,column=0,sticky="nsew")                     
        self.frame_content = ttk.Frame(master)
        self.frame_content.grid(row=0,column=0,sticky="nsew")


        # Submit Button
        ttk.Button(self.frame_content, text='Browse...', command=self.select_file).grid(row =4, column = 1, pady = 20, sticky = E)     
        self.filename_var = StringVar()
        self.filename_var.set("Upload File")


        # Select File Button
        #open_button = ttk.Button(self.frame2, text="Select File", command=self.select_file)
        #open_button.grid(column=1, row=1, sticky=W)
        #open_button['command'] = self.select_file
        ttk.Button(self.frame_content, text='Okay', command=Close).grid(row = 5, column = 1, pady = 20, sticky = E)
        # not working
        self.filename =''
        print(self.filename)

    
    def select_file(self):
        global file
        file = filedialog.askopenfilename(filetypes=[('PDF','*.pdf'),('All files','*.*')])
        self.filename_var.set(file)
  

def main():
    root = Tk()
    Feedback(root)
    root.mainloop()

#if __name__ == "__main__": main() # run the file access


# #### Get First Team

# In[4]:


def get_1st_team(): # Loop through each MDS page and search for the desired text
    
    search_string = '1st Team' 
    for page_number in range(len(pdf_reader.pages)): 
            text = pdf_reader.pages[page_number].extract_text() 
            if search_string in text: 
                page = page_number + 1
    # get table from MDS page, replace NaN with blanks, drop weird unnamed column
    global ft
    ft = pd.DataFrame(tabula.read_pdf(file, pages=page)[0]).replace(np.nan, '')
    ft.drop(ft.filter(regex="Unname"),axis=1, inplace=True) # if col imported "unnamed" then drop it
    pdf_file.close()


# #### Get MDS Submission data

# Get the next turn submission details for this MDS

# In[5]:


def get_MDS_submission_data(): # scan the PDF for first text occurrence of Turn Deadline and extract dataframe 
    global turn_data, duedate, team_id, current_page, season, turn
    pdf_file = open(file, 'rb') # Open the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file) # Create a PDF reader object
    page = [] # set list to append pages to
    search_string = 'Turn Deadline' # set desired searchable text 
    
    for page_number in range(len(pdf_reader.pages)): # search file for text and append each page where this is found to the list
            text = pdf_reader.pages[page_number].extract_text() 
            if search_string in text: 
                script = page_number + 1
                page.append(script)
    
    # top, left, depth, width
    turn_data = tabula.read_pdf(file, area=[0.3*72, 100, 80, 180], pages=page[0])[0] # extract data from the table
    
    # set turn deadline
    deadline = list(turn_data.columns.values)
    duedate = str(deadline[0])
    
    team_id = turn_data.iloc[0:1].squeeze()
    current_page = str(page[0])
    
    turn_data = tabula.read_pdf(file, area=[0.58*72, 2.8*72, 1.05*72, 5.46*72], pages=page[0])[0] # extract data from the table
    turn_list = list(turn_data.columns.values)
    data = turn_list[0]
    season = data[22:23] # extract season from MDS submission form
    turn = data[29:] # extract season from MDS submission form


# In[6]:


def get_email(): # get data from pdf 1st page 
    global email
    global mgr
    # top, left, depth, width
    turn_data = tabula.read_pdf(file, area=[2.01*72, 0.74*72, 2.66*72, 2.77*72], pages=1)[0] # extract data from the table
    #print(turn_data)
    email = turn_data.iloc[0:1].squeeze()
    mgr_list = list(turn_data.columns.values)
    mgr = mgr_list[0]


# In[7]:


def get_game():
    global game
    game = os.path.basename(file) # get base file name
    if game[0] != "G": # if file name doesn't start with G
        game = game[7:10] # strip first 2 letters
    else:
        game = game[5:8]


# In[8]:


def get_teamname():
    global team
                                                # top, left, depth, width
    turn_data = tabula.read_pdf(file, area=[0.22*72, 1.45*72, 0.63*72, 6.21*72], pages=[1])[0] # extract data from the table
    turn_list = list(turn_data.columns.values)
    data = turn_list[0]
    team = data[19:] # extract teamname from MDS submission form


# #### Get Last Week's Submission

# In[9]:


def get_last_selection():
    global last_teamz, last_subz, last_tacz   
    mdspage = []
    search_string = 'TeamID' # set desired searchable text 
    
    for page_number in range(len(pdf_reader.pages)): # search file for text and append each page where this is found to the list
            text = pdf_reader.pages[page_number].extract_text() 
            if search_string in text: 
                script = page_number + 1
                mdspage.append(script)
                                           
    # get last week's team submission: top, left, depth, width
    last_teamz = pd.DataFrame(tabula.read_pdf(file, area=[1.7*72, 0.2*72, 5.2*72, 2.24*72], pages=mdspage[0])[0])
    last_teamz.drop(list(last_teamz.filter(regex='Unnamed: 0')), axis=1, inplace=True) # if column exists called "unnamed: 0" - drop it

    # get last week's subs submission: top, left, depth, width
    last_subz = pd.DataFrame(tabula.read_pdf(file, area=[4.25*72, 0.2*72, 5.5*72, 1.8*72], pages=mdspage[0])[0])
    last_subz.drop(list(last_subz.filter(regex='Unnamed: 0')), axis=1, inplace=True) # if column exists called "unnamed: 0" - drop it
    
    # get last week's subs submission: top, left, depth, width
    last_tacz = pd.DataFrame(tabula.read_pdf(file, area=[1.55*72, 5.35*72, 3.5*72, 7.4*72], pages=mdspage[0])[0])
    last_tacz.drop(list(last_tacz.filter(regex='Unnamed: 0')), axis=1, inplace=True) # if column exists called "unnamed: 0" - drop it


# # Execute

# In[10]:


if __name__ == "__main__": main() # run the file access


# In[11]:


pdf_file = open(file, 'rb') # Open the PDF file 
pdf_reader = PyPDF2.PdfReader(pdf_file) # Create a PDF reader object

PV = 30 # set PV threshold for first team
rPV = 30 # set PV threshold for res team
y_PV = 27 # set PV threshold for youth team
print(f'The sorting elves are doing their stuff... hang in there...')
def get_MDS_data():
    get_1st_team()
    get_email()
    get_game()
    get_teamname()
    get_MDS_submission_data()
    get_last_selection()
    pdf_file.close()
get_MDS_data()


print('\nThe next turn deadline is: ' + duedate +
      '\nYour team ID is: ' + team_id +
      '\nYour team name is: ' + team +
      '\nYour manager name is: ' + mgr +
     '\nYour email is: ' + email +
     '\nThe current game is: ' + str(game) +
     '\nThe next turn is: ' + str(turn) +
     '\nThe season for the next MDS is: ' + str(season))


# In[12]:


team_data = {"Deadline": duedate, 
             "TeamID": team_id,
             "Team":team,
             "Manager":mgr,
             "Email":email,
             "Game":game,
             "Turn":turn,
             "Season":season,
            "Filepath": file}

mds_data = pd.DataFrame.from_dict(team_data, orient='index')
mds_data = mds_data.T
mds_data
#with mds_data.ExcelWriter('Show Team.xlsx', sheet="mds_data") as writer:

mds_data.to_csv("Turn Data/Turn Data.csv", mode="w")


# In[13]:


mds_data


# # Data Cleaning

# ## First Team - Data Cleaning

# #### Strip special characters

# Replace any -, + or * in stats

# In[14]:


ft.iloc[:,3:16] = ft.iloc[:,3:16].map(lambda x: x.rstrip('*+-'))


# #### Split First Team into Sections

# Cut into sections

# In[15]:


# https://stackoverflow.com/questions/71520066/split-a-dataframe-with-multiple-header-rows-into-unique-dataframes
f = ft.eq(ft.columns)
groups = [g.reset_index(drop=True) for _, g in ft[~f.iloc[:, 0]].groupby(f.cumsum()[~f.iloc[:, 0]].iloc[:, 0])]
gks = groups[0].drop(index=0)
deff = groups[1].drop(index=0)
mid = groups[2].drop(index=0)
att = groups[3].drop(index=0)
groups = [gks,deff,mid,att]


# #### Split, Rename and reorder cols

# Rename & Split

# In[16]:


#--------------- rename ----------------#

deff = deff.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
mid = mid.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
att = att.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})

#--------------- split ----------------#

gks[['ID', 'Name']] = gks['ID Name'].str.split(' ', n=1, expand=True) # split gk "ID Name"
gks.drop(columns="ID Name",axis=1, inplace=True) # drop "ID Name" which was imported incorrectly
gks = gks[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Dis","Han","Ref","Crs","OA","SA","Conf","P","Fitness"]] # set columns in desired order

deff[['ID', 'Name']] = deff['ID Name'].str.split(' ', n=1, expand=True) # split deff "ID Name"
deff.drop(columns="ID Name",axis=1, inplace=True) # drop "ID Name" which was imported incorrectly
deff = deff[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]] # set columns in desired order

mid[['ID', 'Name']] = mid['ID Name'].str.split(' ', n=1, expand=True) # split mid "ID Name"
mid.drop(columns="ID Name",axis=1, inplace=True) # drop "ID Name" which was imported incorrectly
mid = mid[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]] # set columns in desired order

att[['ID', 'Name']] = att['ID Name'].str.split(' ', n=1, expand=True) # split att "ID Name"
att.drop(columns="ID Name",axis=1, inplace=True) # drop "ID Name" which was imported incorrectly
att = att[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]] # set columns in desired order


# Change stats to integers

# In[17]:


# change gk stat columns to integers
gks_columns = gks.columns.to_list()[4:16]
for i in gks_columns:
   gks[i] = gks[i].astype('int32')

# change deff stat columns to integers
deff_columns = deff.columns.to_list()[4:16]
for i in deff_columns:
   deff[i] = deff[i].astype('int32')

# change mid stat columns to integers
mid_columns = mid.columns.to_list()[4:16]
for i in mid_columns:
   mid[i] = mid[i].astype('int32')

# change att stat columns to integers
att_columns = att.columns.to_list()[4:16]
for i in att_columns:
    att[i] = att[i].astype('int32')
   
#ft


# #### Injured, Suspended & Unfit Players

# Add inj players to new dataframe

# In[18]:


# Identify injured players
inj = ft.groupby("Fitness")
if "Inj" in inj.groups.keys():
    injured = inj.get_group("Inj")
    print(f"Injuries {injured}")
else:
    print("No injured players this week")

# Identify suspended players
sus = ft.groupby("Fitness")
if "Sus" in sus.groups.keys():
    suspended = sus.get_group("Sus")
    print(f"Suspended: {suspended}")
else:
    print("No suspended players this week")


# Remove Injured Players

# In[19]:


#inj = ft['Fitness'] == 'Inj'
#ft = ft[~inj]


# #### Left, Right, Both-Footed

# Group Players by Foot

# In[20]:


empty = ["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"]

Foot = deff.groupby("Foot") # get midfield groups by their "Foot"

# RIGHT FOOTED - set groups by foot >> use logic to work out if any players are NOT both footed
if "R" in Foot.groups.keys():
    deff_R = Foot.get_group("R")
else:
    deff_RP = pd.DataFrame(empty)
    
if "B" in Foot.groups.keys():
    deff_B = Foot.get_group("B")
else:
    deff_B = pd.DataFrame()
# Right postional players = Merge R and B footed players together
if deff_B.empty:
    deff_RP = deff_R
else:
    deff_RP = pd.concat([deff_R, deff_B])

# LEFT FOOTED - set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    deff_L = Foot.get_group("L")
else:
    pd.DataFrame(empty)
    
if "B" in Foot.groups.keys():
    deff_B = Foot.get_group("B")
else:
    deff_B = pd.DataFrame()
# Left postional players = Merge L and B footed players together
if deff_B.empty:
    deff_LP = deff_L
else:
    deff_LP = pd.concat([deff_L, deff_B])


# midfield

# In[21]:


Foot = mid.groupby("Foot") # get midfield groups by their "Foot"

# RIGHT FOOTED
if "R" in Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    mid_R = Foot.get_group("R")
else:
    mid_R = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    mid_B = Foot.get_group("B")
else:
    mid_B = pd.DataFrame()

# Right postional players = Merge R and B footed players together
if mid_B.empty:
    mid_RP = mid_R
else:
    mid_RP = [mid_R, mid_B]
    mid_RP = pd.concat(mid_RP)
# show mid right positionals

# LEFT FOOTED PLAYERS
# set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    mid_L = Foot.get_group("L")
else:
    mid_L = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    mid_B = Foot.get_group("B") # get both footed players
else:
    mid_B = pd.DataFrame() #set mid_B as empty df
    
# Left postional players = Merge L and B footed players together
if mid_B.empty:
    mid_LP = mid_L
else:
    mid_LP = [mid_L, mid_B]
    mid_LP = pd.concat(mid_LP)


# ------------- RARE case where players aren't left or right footed
if mid_LP.empty:
    mid_LP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass
    
if mid_RP.empty:
    mid_RP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass


# Attack

# In[22]:


Foot = att.groupby("Foot") # get attackers groups by their "Foot"

# RIGHT FOOTED
if "R" in Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    Att_R = Foot.get_group("R")
else:
    Att_R = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    Att_B = Foot.get_group("B")
else:
    Att_B = pd.DataFrame()

# Right postional players = Merge R and B footed players together
if Att_B.empty:
    Att_RP = Att_R
else:
    Att_RP = [Att_R, Att_B]
    Att_RP = pd.concat(Att_RP)

# LEFT FOOTED PLAYERS
# set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    Att_L = Foot.get_group("L")
else:
    Att_L = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    Att_B = Foot.get_group("B") # get both footed players
else:
    Att_B = pd.DataFrame() #set Att_B as empty df
    
# Left postional players = Merge L and B footed players together
if Att_B.empty:
    Att_LP = Att_L
else:
    Att_LP = [Att_L, Att_B]
    Att_LP = pd.concat(Att_LP)

# ------------- RARE case where players aren't left or right footed
if Att_LP.empty:
    Att_LP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass

if Att_RP.empty:
    Att_RP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass


# ### Calculate Positional Values

# In[23]:


gks['GK'] = gks[['Dis', 'Han', 'Ref','Crs']].sum(axis = 1, skipna = True)

deff['CB'] = deff[['Hea', 'Str', 'Tac','Jud']].sum(axis = 1, skipna = True) # create new col labelled CB PV and sum the given values into it. Skip empty cells
deff['LB'] = deff_LP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True); deff['LB'] = deff['LB'].fillna(0)
deff['RB'] = deff_RP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True); deff['RB'] = deff['RB'].fillna(0) 
deff['SW'] = deff[['Pas', 'Con', 'Tac','Jud']].sum(axis = 1, skipna = True)
deff['LWB'] = deff_LP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1); deff['LWB'] = deff['LWB'].fillna(0)
deff['RWB'] = deff_RP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1); deff['RWB'] = deff['RWB'].fillna(0)

mid['CM'] = mid[['Pas', 'Sta', 'Hea','Tac']].sum(axis = 1, skipna = True)
mid['AM'] = mid[['Str', 'Agg', 'Tac','Jud']].sum(axis = 1, skipna = True)
mid['PL'] = mid[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)
mid['FR'] = mid[['Sho', 'Mov', 'Pas','Con']].sum(axis = 1, skipna = True)
mid['RW'] = mid_RP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1); mid['RW'] = mid['RW'].fillna(0)
mid['LW'] = mid_LP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1); mid['LW'] = mid['LW'].fillna(0)

att['LF'] = Att_LP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1); att['LF'] = att['LF'].fillna(0)
att['RF'] = Att_RP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1); att['RF'] = att['RF'].fillna(0)
att['IF'] = att[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)
att['CF'] = att[['Sho', 'Mov', 'Str','Agg']].sum(axis = 1, skipna = True)
att['TM'] = att[['Con', 'Hea', 'Str','Agg']].sum(axis = 1, skipna = True)


# #### Set PV threshold

# In[24]:


def set_1st_team_PV():     # clear weak roles  

    deff['CB'] = deff['CB'].astype(int); deff['CB'] = np.where(deff['CB'] < PV, "", deff['CB'])
    deff['SW'] = deff['SW'].astype(int); deff['SW'] = np.where(deff['SW'] < PV, "", deff['SW'])
    deff['LWB'] = deff['LWB'].astype(int); deff['LWB'] = np.where(deff['LWB'] < PV, "", deff['LWB'])

    deff['RWB'] = deff['RWB'].astype(int); deff['RWB'] = np.where(deff['RWB'] < PV, "", deff['RWB'])
    deff['LB'] = deff['LB'].astype(int); deff['LB'] = np.where(deff['LB'] < PV, "", deff['LB'])
    deff['RB'] = deff['RB'].astype(int); deff['RB'] = np.where(deff['RB'] < PV, "", deff['RB'])
    
    mid['CM'] = mid['CM'].astype(int); mid['CM'] = np.where(mid['CM'] < PV, "", mid['CM'])
    mid['AM'] = np.where(mid['AM'] < PV, "", mid['AM'])
    mid['PL'] = np.where(mid['PL'] < PV, "", mid['PL'])
    mid['FR'] = np.where(mid['FR'] < PV, "", mid['FR'])
    mid['LW'] = mid['LW'].astype(int); mid['LW'] = np.where(mid['LW'] < PV, "", mid['LW'])
    mid['RW'] = mid['RW'].astype(int); mid['RW'] = np.where(mid['RW'] < PV, "", mid['RW'])
    
    att['LF'] = att['LF'].astype(int); att['LF'] = np.where(att['LF'] < PV, "", att['LF'])
    att['RF'] = att['RF'].astype(int); att['RF'] = np.where(att['RF'] < PV, "", att['RF'])
    att['IF'] = np.where(att['IF'] < PV, "", att['IF'])
    att['TM'] = np.where(att['TM'] < PV, "", att['TM'])
    att['CF'] = np.where(att['CF'] < PV, "", att['CF'])

set_1st_team_PV()


# ## Reserve Team - Data Cleaning

# #### Locate Reserve Team

# In[25]:


# Open the PDF file 
pdf_file = open(file, 'rb') 
     
# Create a PDF reader object 
pdf_reader = PyPDF2.PdfReader(pdf_file) 
     
# Loop through each MDS page and search for the desired text 
search_string = '1st Team' 
for page_number in range(len(pdf_reader.pages)): 
        text = pdf_reader.pages[page_number].extract_text() 
        if search_string in text: 
            page = page_number + 3
# get table from MDS page, replace NaN with blanks, drop weird unnamed column
res = pd.DataFrame(tabula.read_pdf(file, pages=page)[0]).replace(np.nan, '')
res.drop(res.filter(regex="Unname"),axis=1, inplace=True)
pdf_file.close()


# #### Strip special characters

# In[26]:


res.iloc[:,3:16] = res.iloc[:,3:16].map(lambda x: x.rstrip('*+-'))


# #### Split Reserve Team into Sections

# In[27]:


# https://stackoverflow.com/questions/71520066/split-a-dataframe-with-multiple-header-rows-into-unique-dataframes
r = res.eq(res.columns)
r_groups = [g.reset_index(drop=True) for _, g in res[~r.iloc[:, 0]].groupby(r.cumsum()[~r.iloc[:, 0]].iloc[:, 0])]
r_gks = r_groups[0].drop(index=0)
r_deff = r_groups[1].drop(index=0)
r_mid = r_groups[2].drop(index=0)
r_att = r_groups[3].drop(index=0)
# rename cols
r_deff = r_deff.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
r_mid = r_mid.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
r_att = r_att.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})


# #### Split, Rename and reorder cols

# Ensure ID and Name are split

# In[28]:


# split gk "ID Name"
r_gks[['ID', 'Name']] = r_gks['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
r_gks.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
r_gks = r_gks[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Dis","Han","Ref","Crs","OA","SA","Conf","P","Fitness"]]

# split deff "ID Name"
r_deff[['ID', 'Name']] = r_deff['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
r_deff.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
r_deff = r_deff[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]

# split mid "ID Name"
r_mid[['ID', 'Name']] = r_mid['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
r_mid.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
r_mid = r_mid[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]

# split att "ID Name"
r_att[['ID', 'Name']] = r_att['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
r_att.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
r_att = r_att[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]


# Stats to integers

# In[29]:


# change gk stat columns to integers
r_gks_columns = r_gks.columns.to_list()[4:16]
for i in r_gks_columns:
   r_gks[i] = r_gks[i].astype('int32')

# change deff stat columns to integers
r_deff_columns = r_deff.columns.to_list()[4:16]
for i in r_deff_columns:
   r_deff[i] = r_deff[i].astype('int32')

# change mid stat columns to integers
r_mid_columns = r_mid.columns.to_list()[4:16]
for i in r_mid_columns:
   r_mid[i] = r_mid[i].astype('int32')

# change att stat columns to integers
r_att_columns = r_att.columns.to_list()[4:16]
for i in r_att_columns:
    r_att[i] = r_att[i].astype('int32')


# #### Injuries

# In[30]:


# Identify injured players
r_inj = res.groupby("Fitness")
if "Inj" in r_inj.groups.keys():
    r_injured = r_inj.get_group("Inj")
    print("Injuries")
else:
    print("No injured players this week")

# Identify suspended players
r_sus = res.groupby("Fitness")
if "Sus" in r_sus.groups.keys():
    r_suspended = r_sus.get_group("Sus")
    print("Suspension")
else:
    print("No suspended players this week")


# #### Reserve: Left, Right, Both-Footed

# Defenders

# In[31]:


data_cols = ["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"]
r_Foot = r_deff.groupby("Foot") # get midfield groups by their "Foot"

# ====== Both Footed =======#
if "B" in r_Foot.groups.keys():
    r_deff_B = r_Foot.get_group("B")
else:
    r_deff_B = pd.DataFrame(columns = data_cols)

# ====== Right Footed =======#
if ("R" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_deff_R = r_Foot.get_group("R")
    r_deff_RP = pd.concat([r_deff_R,r_deff_B])
else:
    r_deff_RP = pd.DataFrame(columns = data_cols)

# ====== Left Footed =======#
if ("L" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_deff_L = r_Foot.get_group("L")
    r_deff_LP = pd.concat([r_deff_L,r_deff_B])
else:
    r_deff_LP = pd.DataFrame(columns = data_cols)


# midfielders

# In[32]:


r_Foot = r_mid.groupby("Foot") # get midfield groups by their "Foot"

# ====== Both Footed =======#
if "B" in r_Foot.groups.keys():
    r_mid_B = r_Foot.get_group("B")
else:
    r_mid_B = pd.DataFrame(columns = data_cols)

# ====== Right Footed =======#
if ("R" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_mid_R = r_Foot.get_group("R")
    r_mid_RP = pd.concat([r_mid_R,r_mid_B])
else:
    r_mid_RP = pd.DataFrame(columns = data_cols)

# ====== Left Footed =======#
if ("L" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_mid_L = r_Foot.get_group("L")
    r_mid_LP = pd.concat([r_mid_L,r_mid_B])
else:
    r_mid_LP = pd.DataFrame(columns = data_cols)


# Strikers

# In[33]:


r_Foot = r_att.groupby("Foot") # get midfield groups by their "Foot"

# ====== Both Footed =======#
if "B" in r_Foot.groups.keys():
    r_att_B = r_Foot.get_group("B")
else:
    r_att_B = pd.DataFrame(columns = data_cols)

# ====== Right Footed =======#
if ("R" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_att_R = r_Foot.get_group("R")
    r_att_RP = pd.concat([r_att_R,r_att_B])
else:
    r_att_RP = pd.DataFrame(columns = data_cols)

# ====== Left Footed =======#
if ("L" or "B") in r_Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    r_att_L = r_Foot.get_group("L")
    r_att_LP = pd.concat([r_att_L,r_att_B])
else:
    r_att_LP = pd.DataFrame(columns = data_cols)


# ### Reserves: Calculate PV

# #### Reserve GKs

# In[34]:


# sum stat columns 
r_gks['GK'] = r_gks[['Dis', 'Han', 'Ref','Crs']].sum(axis = 1, skipna = True)


# #### Reserve Defence

# In[35]:


# CB PV
# create new col labelled CB PV and sum the given values into it. Skip empty cells
r_deff['CB'] = r_deff[['Hea', 'Str', 'Tac','Jud']].sum(axis = 1, skipna = True)

# Leftback PV
# create new col labelled FB PV and sum the given values into it. Skip empty cells
r_deff['LB'] = r_deff_LP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True)
# fill NaN with 0, convert to int and replace 0 with ""
r_deff['LB'] = r_deff['LB'].fillna(0)

# Rightback PV
# create new col labelled FB PV and sum the given values into it. Skip empty cells
r_deff['RB'] = r_deff_RP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True)
# fill NaN with 0, convert to int and replace 0 with ""
r_deff['RB'] = r_deff['RB'].fillna(0)

# SW PV
# create new col labelled CB PV and sum the given values into it. Skip empty cells
r_deff['SW'] = r_deff[['Pas', 'Con', 'Tac','Jud']].sum(axis = 1, skipna = True)

# Left Wingback PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_deff['LWB'] = r_deff_LP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_deff['LWB'] = r_deff['LWB'].fillna(0)

# Left Wingback PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_deff['RWB'] = r_deff_RP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_deff['RWB'] = r_deff['RWB'].fillna(0)


# #### Reserve midfield

# In[36]:


# CM PV
# create new col labelled CB PV and sum the given values into it. Skip empty cells
r_mid['CM'] = r_mid[['Pas', 'Sta', 'Hea','Tac']].sum(axis = 1, skipna = True)

# AM PV
# create new col labelled FB PV and sum the given values into it. Skip empty cells
r_mid['AM'] = r_mid[['Str', 'Agg', 'Tac','Jud']].sum(axis = 1, skipna = True)

# PL PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_mid['PL'] = r_mid[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)

# FR PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_mid['FR'] = r_mid[['Sho', 'Mov', 'Pas','Con']].sum(axis = 1, skipna = True)

# Right Winger PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_mid['RW'] = r_mid_RP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_mid['RW'] = r_mid['RW'].fillna(0)

# Left Winger PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_mid['LW'] = r_mid_LP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_mid['LW'] = r_mid['LW'].fillna(0)


# In[37]:


# Left Forward PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_att['LF'] = r_att_LP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_att['LF'] = r_att['LF'].fillna(0)

# Right Forward PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_att['RF'] = r_att_RP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
r_att['RF'] = r_att['RF'].fillna(0)

# IF PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_att['IF'] = r_att[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)

# CF PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_att['CF'] = r_att[['Sho', 'Mov', 'Str','Agg']].sum(axis = 1, skipna = True)

# TM PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
r_att['TM'] = r_att[['Con', 'Hea', 'Str','Agg']].sum(axis = 1, skipna = True)


# #### Set PV threshold

# In[38]:


# clear weak roles
r_deff['CB'] = r_deff['CB'].astype(int); r_deff['CB'] = np.where(r_deff['CB'] < rPV, "", r_deff['CB'])
r_deff['SW'] = r_deff['SW'].astype(int); r_deff['SW'] = np.where(r_deff['SW'] < rPV, "", r_deff['SW'])

r_mid['CM'] = np.where(r_mid['CM'] < rPV, "", r_mid['CM'])
r_mid['AM'] = np.where(r_mid['AM'] < rPV, "", r_mid['AM'])
r_mid['PL'] = np.where(r_mid['PL'] < rPV, "", r_mid['PL'])
r_mid['FR'] = np.where(r_mid['FR'] < rPV, "", r_mid['FR'])

r_att['IF'] = np.where(r_att['IF'] < rPV, "", r_att['IF'])
r_att['TM'] = np.where(r_att['TM'] < rPV, "", r_att['TM'])
r_att['CF'] = np.where(r_att['CF'] < rPV, "", r_att['CF'])

r_deff['LB'] = r_deff['LB'].astype(int); r_deff['LB'] = np.where(r_deff['LB'] < rPV, "", r_deff['LB'])
r_deff['RB'] = r_deff['RB'].astype(int); r_deff['RB'] = np.where(r_deff['RB'] < rPV, "", r_deff['RB'])
r_deff['LWB'] = r_deff['LWB'].astype(int); r_deff['LWB'] = np.where(r_deff['LWB'] < rPV, "", r_deff['LWB'])
r_deff['RWB'] = r_deff['RWB'].astype(int); r_deff['RWB'] = np.where(r_deff['RWB'] < rPV, "", r_deff['RWB'])
r_mid['LW'] = r_mid['LW'].astype(int); r_mid['LW'] = np.where(r_mid['LW'] < rPV, "", r_mid['LW'])
r_mid['RW'] = r_mid['RW'].astype(int); r_mid['RW'] = np.where(r_mid['RW'] < rPV, "", r_mid['RW'])
r_att['LF'] = r_att['LF'].astype(int); r_att['LF'] = np.where(r_att['LF'] < rPV, "", r_att['LF'])
r_att['RF'] = r_att['RF'].astype(int); r_att['RF'] = np.where(r_att['RF'] < rPV, "", r_att['RF'])


# ## Youth Team - Data Cleaning

# In[39]:


# Open the PDF file 
pdf_file = open(file, 'rb') 
     
# Create a PDF reader object 
pdf_reader = PyPDF2.PdfReader(pdf_file) 
     
# Loop through each MDS page and search for the desired text 
search_string = '1st Team' 
for page_number in range(len(pdf_reader.pages)): 
        text = pdf_reader.pages[page_number].extract_text() 
        if search_string in text: 
            page = page_number + 5
# get table from MDS page, replace NaN with blanks, drop weird unnamed column
yt = pd.DataFrame(tabula.read_pdf(file, pages=page)[0]).replace(np.nan, '')
yt.drop(yt.filter(regex="Unname"),axis=1, inplace=True)
pdf_file.close()


# In[40]:


yt.iloc[:,3:16] = yt.iloc[:,3:16].map(lambda x: x.rstrip('*+-')) # remove special characters


# #### Split First Team into Sections

# Cut into sections

# In[41]:


# https://stackoverflow.com/questions/71520066/split-a-dataframe-with-multiple-header-rows-into-unique-dataframes
y = yt.eq(yt.columns)
y_groups = [g.reset_index(drop=True) for _, g in yt[~y.iloc[:, 0]].groupby(y.cumsum()[~y.iloc[:, 0]].iloc[:, 0])]
y_gks = y_groups[0].drop(index=0)
y_deff = y_groups[1].drop(index=0)
y_mid = y_groups[2].drop(index=0)
y_att = y_groups[3].drop(index=0)


# #### Split, Rename and reorder cols

# Rename

# In[42]:


# rename cols
y_deff = y_deff.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
y_mid = y_mid.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})
y_att = y_att.rename(columns={'Dis': 'Agg', 'Han': 'Tac', 'Ref':'Jud','Crs':'Vis'})


# Split

# In[43]:


y_gks[['ID', 'Name']] = y_gks['ID Name'].str.split(' ', n=1, expand=True)
y_gks.drop(columns="ID Name",axis=1, inplace=True)
y_gks = y_gks[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Dis","Han","Ref","Crs","OA","SA","Conf","P","Fitness"]]

# split deff "ID Name"
y_deff[['ID', 'Name']] = y_deff['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
y_deff.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
y_deff = y_deff[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]

# split mid "ID Name"
y_mid[['ID', 'Name']] = y_mid['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
y_mid.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
y_mid = y_mid[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]

# split att "ID Name"
y_att[['ID', 'Name']] = y_att['ID Name'].str.split(' ', n=1, expand=True)
# drop "ID Name" which was imported incorrectly
y_att.drop(columns="ID Name",axis=1, inplace=True)
# set columns in desired order
y_att = y_att[["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","SA","Conf","P","Fitness"]]


# Change stats to integers

# In[44]:


# change gk stat columns to integers
y_gks_columns = y_gks.columns.to_list()[4:16]
for i in y_gks_columns:
   y_gks[i] = y_gks[i].astype(int)

# change deff stat columns to integers
y_deff_columns = y_deff.columns.to_list()[4:16]
for i in y_deff_columns:
   y_deff[i] = y_deff[i].astype(int)

# change mid stat columns to integers
y_mid_columns = y_mid.columns.to_list()[4:16]
for i in y_mid_columns:
   y_mid[i] = y_mid[i].astype(int)

# change att stat columns to integers
y_att_columns = y_att.columns.to_list()[4:16]
for i in y_att_columns:
    y_att[i] = y_att[i].astype(int)


# #### Injured, Suspended & Unfit Players

# Add inj players to new dataframe

# In[45]:


# Identify injured players
y_inj = yt.groupby("Fitness")
if "Inj" in y_inj.groups.keys():
    y_injured = y_inj.get_group("Inj")
    print(f"Injured youth players... \n {y_injured}")
else:
    print("No injured youth players this week")

# Identify suspended players
y_sus = yt.groupby("Fitness")
if "Sus" in y_sus.groups.keys():
    y_suspended = y_sus.get_group("Sus")
    print(f"Suspended youth players... \n {y_suspended}")
else:
    print("No suspended youth players this week")


# Remove Injured Players

# In[46]:


#inj = ft['Fitness'] == 'Inj'
#ft = ft[~inj]


# #### Left, Right, Both-Footed

# Group Players by Foot

# In[47]:


# get midfield groups by their "Foot"
Foot = y_deff.groupby("Foot")

# RIGHT FOOTED
# set groups by foot >> use logic to work out if any players are NOT both footed
if "R" in Foot.groups.keys():
    y_deff_R = Foot.get_group("R")
else:
    y_deff_R = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_deff_B = Foot.get_group("B")
else:
    y_deff_B = pd.DataFrame()
# Right postional players = Merge R and B footed players together
if y_deff_B.empty:
    y_deff_RP = y_deff_R
else:
    y_deff_RP = [y_deff_R, y_deff_B]
    y_deff_RP = pd.concat(y_deff_RP)
# show mid right positionals
y_deff_RP

# LEFT FOOTED
# set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    y_deff_L = Foot.get_group("L")
else:
    y_deff_L = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_deff_B = Foot.get_group("B")
else:
    y_deff_B = pd.DataFrame()
    
# Left postional players = Merge L and B footed players together
if y_deff_B.empty:
    y_deff_LP = y_deff_L
else:
    y_deff_LP = [y_deff_L, y_deff_B]
    y_deff_LP = pd.concat(y_deff_LP)
# show mid right positionals

# ------------- RARE case where players aren't left or right footed
if y_deff_LP.empty:
    y_deff_LP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass

if y_deff_RP.empty:
    y_deff_RP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass


# midfield

# In[48]:


Foot = y_mid.groupby("Foot") # get y_midfield groups by their "Foot"

# RIGHT FOOTED
if "R" in Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    y_mid_R = Foot.get_group("R")
else:
    y_mid_R = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_mid_B = Foot.get_group("B")
else:
    y_mid_B = pd.DataFrame()

# Right postional players = Merge R and B footed players together
if y_mid_B.empty:
    y_mid_RP = y_mid_R
else:
    y_mid_RP = [y_mid_R, y_mid_B]
    y_mid_RP = pd.concat(y_mid_RP)
# show y_mid right positionals

# LEFT FOOTED PLAYERS
# set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    y_mid_L = Foot.get_group("L")
else:
    y_mid_L = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_mid_B = Foot.get_group("B") # get both footed players
else:
    y_mid_B = pd.DataFrame() #set y_mid_B as empty df
    
# Left postional players = Merge L and B footed players together
if y_mid_B.empty:
    y_mid_LP = y_mid_L
else:
    y_mid_LP = [y_mid_L, y_mid_B]
    y_mid_LP = pd.concat(y_mid_LP)


# ------------- RARE case where players aren't left or right footed
if y_mid_LP.empty:
    y_mid_LP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass
    
if y_mid_RP.empty:
    y_mid_RP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass


# Attack

# In[49]:


Foot = y_att.groupby("Foot") # get y_attackers groups by their "Foot"

# RIGHT FOOTED
if "R" in Foot.groups.keys(): # set groups by foot >> use logic to work out if any players are NOT both footed
    y_Att_R = Foot.get_group("R")
else:
    y_Att_R = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_Att_B = Foot.get_group("B")
else:
    y_Att_B = pd.DataFrame()

# Right postional players = Merge R and B footed players together
if y_Att_B.empty:
    y_Att_RP = y_Att_R
else:
    y_Att_RP = [y_Att_R, y_Att_B]
    y_Att_RP = pd.concat(y_Att_RP)

# LEFT FOOTED PLAYERS
# set groups by foot >> use logic to work out if any players are NOT both footed
if "L" in Foot.groups.keys():
    y_Att_L = Foot.get_group("L")
else:
    y_Att_L = pd.DataFrame()
    
if "B" in Foot.groups.keys():
    y_Att_B = Foot.get_group("B") # get both footed players
else:
    y_Att_B = pd.DataFrame() #set y_Att_B as empty df
    
# Left postional players = Merge L and B footed players together
if y_Att_B.empty:
    y_Att_LP = y_Att_L
else:
    y_Att_LP = [y_Att_L, y_Att_B]
    y_Att_LP = pd.concat(y_Att_LP)

# ------------- RARE case where players aren't left or right footed
if y_Att_LP.empty:
    y_Att_LP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass

if y_Att_RP.empty:
    y_Att_RP = pd.DataFrame(columns =["ID", "Name", "Age", "Foot", "Sho", "Mov","Pas","Con","Spe","Sta","Hea","Str","Agg","Tac","Jud","Vis","OA","Conf","P","Fitness"])
else:
    pass


# ### Calculate Positional Values

# #### Goalkeepers

# In[50]:


# sum stat columns 
y_gks['GK'] = y_gks[['Dis', 'Han', 'Ref','Crs']].sum(axis = 1, skipna = True)


# #### Defence

# In[51]:


# CB PV
# create new col labelled CB PV and sum the given values into it. Skip empty cells
y_deff['CB'] = y_deff[['Hea', 'Str', 'Tac','Jud']].sum(axis = 1, skipna = True)

# Leftback PV
# create new col labelled FB PV and sum the given values into it. Skip empty cells
y_deff['LB'] = y_deff_LP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True)
# fill NaN with 0, convert to int and replace 0 with ""
y_deff['LB'] = y_deff['LB'].fillna(0)

# Rightback PV
y_deff['RB'] = y_deff_RP[['Spe', 'Sta', 'Agg','Tac']].sum(axis = 1, skipna=True)
y_deff['RB'] = y_deff['RB'].fillna(0)
y_deff['SW'] = y_deff[['Pas', 'Con', 'Tac','Jud']].sum(axis = 1, skipna = True)

# Left Wingback PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_deff['LWB'] = y_deff_LP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
y_deff['LWB'] = y_deff['LWB'].fillna(0)

# Right Wingback PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_deff['RWB'] = y_deff_RP[['Mov', 'Pas', 'Spe','Sta']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
y_deff['RWB'] = y_deff['RWB'].fillna(0)


# #### midfield

# In[52]:


y_mid['CM'] = y_mid[['Pas', 'Sta', 'Hea','Tac']].sum(axis = 1, skipna = True)
y_mid['AM'] = y_mid[['Str', 'Agg', 'Tac','Jud']].sum(axis = 1, skipna = True)
y_mid['PL'] = y_mid[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)
y_mid['FR'] = y_mid[['Sho', 'Mov', 'Pas','Con']].sum(axis = 1, skipna = True)
y_mid['RW'] = y_mid_RP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1); y_mid['RW'] = y_mid['RW'].fillna(0)
y_mid['LW'] = y_mid_LP[['Pas', 'Con', 'Spe','Sta']].sum(axis = 1); y_mid['LW'] = y_mid['LW'].fillna(0)


# #### Attack

# In[53]:


# Left Forward PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_att['LF'] = y_Att_LP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
y_att['LF'] = y_att['LF'].fillna(0)

# Right Forward PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_att['RF'] = y_Att_RP[['Sho', 'Mov', 'Con','Spe']].sum(axis = 1)
# fill NaN with 0, convert to int and replace 0 with ""
y_att['RF'] = y_att['RF'].fillna(0)

# IF PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_att['IF'] = y_att[['Pas', 'Con', 'Jud','Vis']].sum(axis = 1, skipna = True)

# CF PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_att['CF'] = y_att[['Sho', 'Mov', 'Str','Agg']].sum(axis = 1, skipna = True)

# TM PV
# create new col labelled WB PV and sum the given values into it. Skip empty cells
y_att['TM'] = y_att[['Con', 'Hea', 'Str','Agg']].sum(axis = 1, skipna = True)


# #### Set PV threshold

# In[54]:


def set_yth_team_PV():
    # clear weak roles  
    y_deff['CB'] = y_deff['CB'].astype(int); y_deff['CB'] = np.where(y_deff['CB'] < y_PV, "", y_deff['CB'])
    y_deff['SW'] = y_deff['SW'].astype(int); y_deff['SW'] = np.where(y_deff['SW'] < y_PV, "", y_deff['SW'])
    y_deff['LWB'] = y_deff['LWB'].astype(int); y_deff['LWB'] = np.where(y_deff['LWB'] < y_PV, "", y_deff['LWB'])

    
    y_deff['RWB'] = y_deff['RWB'].astype(int); y_deff['RWB'] = np.where(y_deff['RWB'] < y_PV, "", y_deff['RWB'])
    y_deff['LB'] = y_deff['LB'].astype(int); y_deff['LB'] = np.where(y_deff['LB'] < y_PV, "", y_deff['LB'])
    y_deff['RB'] = y_deff['RB'].astype(int); y_deff['RB'] = np.where(y_deff['RB'] < y_PV, "", y_deff['RB'])
    
    y_mid['CM'] = y_mid['CM'].astype(int); y_mid['CM'] = np.where(y_mid['CM'] < y_PV, "", y_mid['CM'])
    y_mid['AM'] = np.where(y_mid['AM'] < y_PV, "", y_mid['AM'])
    y_mid['PL'] = np.where(y_mid['PL'] < y_PV, "", y_mid['PL'])
    y_mid['FR'] = np.where(y_mid['FR'] < y_PV, "", y_mid['FR'])
    y_mid['LW'] = y_mid['LW'].astype(int); y_mid['LW'] = np.where(y_mid['LW'] < y_PV, "", y_mid['LW'])
    y_mid['RW'] = y_mid['RW'].astype(int); y_mid['RW'] = np.where(y_mid['RW'] < y_PV, "", y_mid['RW'])
    
    
    y_att['LF'] = y_att['LF'].astype(int); y_att['LF'] = np.where(y_att['LF'] < y_PV, "", y_att['LF'])
    y_att['RF'] = y_att['RF'].astype(int); y_att['RF'] = np.where(y_att['RF'] < y_PV, "", y_att['RF'])
    y_att['IF'] = np.where(y_att['IF'] < y_PV, "", y_att['IF'])
    y_att['TM'] = np.where(y_att['TM'] < y_PV, "", y_att['TM'])
    y_att['CF'] = np.where(y_att['CF'] < y_PV, "", y_att['CF'])

set_yth_team_PV()


# ## Write to Excel

# #### Export player stats to Excel

# In[55]:


import openpyxl

def export_to_excel():
    x=1
    while x == 1:
        file2 = "Turn Data/Show Team.xlsx"
        with pd.ExcelWriter(file2) as writer:
            gks.to_excel(writer, sheet_name="gks",index=True)
            deff.to_excel(writer, sheet_name="deff",index=True)
            mid.to_excel(writer, sheet_name="mid",index=True)
            att.to_excel(writer, sheet_name="att",index=True)
            r_gks.to_excel(writer, sheet_name="r_gks",index=True)
            r_deff.to_excel(writer, sheet_name="r_deff",index=True)
            r_mid.to_excel(writer, sheet_name="r_mid",index=True)
            r_att.to_excel(writer, sheet_name="r_att",index=True)
            y_gks.to_excel(writer, sheet_name="y_gks",index=True)
            y_deff.to_excel(writer, sheet_name="y_deff",index=True)
            y_mid.to_excel(writer, sheet_name="y_mid",index=True)
            y_att.to_excel(writer, sheet_name="y_att",index=True)
            x+=1
    else:
        pass

export_to_excel()


# #### Export Match Ratings

# In[56]:


print("Gathering awesome player scores... please standby for raw epicness")
time.sleep(2)
filepath = "Turn Data/Turn Data.csv"

pdf_file = open(file, 'rb') # Open the PDF file
pdf_reader = PyPDF2.PdfReader(pdf_file) # Create a PDF reader object
MR = []
MR.clear()
search_string = 'Shots on Target' # set desired searchable text 

for page_number in range(len(pdf_reader.pages)): # search file for text and append each page where this is found to the list
        text = pdf_reader.pages[page_number].extract_text() 
        if search_string in text: 
            script = page_number + 1
            MR.append(script)
    
print(f"match reports detected on pages {MR}")


# In[57]:


plist = []
def send(i):
    
    reader = PdfReader(file)
    
    page = reader.pages
    
                
    # get away team stats accounting for the chance that no events happened
    MRL = tabula.read_pdf(file, area=[2.8*72, 5*72, 5.35*72, 8*72], pages=i, pandas_options={'header': None})[0] # extract data from the table [area = top, left, bottom, right]
    cols = len(MRL.axes[1])
    if cols == 4:
        MRL.columns = ['Name (H)', 'Pos (H)', 'Rating (H)', "Event (H)"]
    elif cols == 3:
        MRL.columns = ['Name (H)', 'Pos (H)', 'Rating (H)']
        MRL["Event (H)"] = ""
    else:
        pass
    MRL = MRL.fillna("")

    # get away team stats accounting for the chance that no events happened
    MRR = tabula.read_pdf(file, area=[2.7*72, 0.64*72, 5.35*72, 3.31*72], pages=i, pandas_options={'header': None})[0] # extract data from the table [area = top, left, bottom, right]
    cols = len(MRR.axes[1])
    if cols == 4:
        MRR.columns = ['Name (A)', 'Pos (A)', 'Rating (A)', "Event (A)"]
    elif cols == 3:
        MRR.columns = ['Name (A)', 'Pos (A)', 'Rating (A)']
        MRR["Event (A)"] = ""
    else:
        pass
    MRR = MRR.fillna("")


    t = pd.concat([MRL,MRR],axis=1)

    new_index = max(t.index) + 1
    t.loc[new_index] = ''

    plist.append(t)

i = 0
while i < len(MR):
    result = send(MR[i])
    i+=1

df = pd.concat(plist)
turn_now = int(turn) -1 
df.to_csv(f"Match Ratings/{str(team)} team ratings for S{str(season)} T{str(turn_now)}.csv")
print(df)
time.sleep(1)
print("\nLook at how well you did. Go you!")
time.sleep(1)
print("\nMatch ratings output to ratings folder")
time.sleep(5)

#https://python-forum.io/thread-23500.html


# In[ ]:


time.sleep(2)
print(f"Thankyou for using whatever this UE companion app is {mgr}. You're all done. The snotlings have deposited your treasure into Match Ratings.")
time.sleep(2)
print("\nIf you scouted using the UE Scouting Tool last week, your scouts analysis will be ready to execute in Jupyter Lab")
time.sleep(5)


# In[ ]:




