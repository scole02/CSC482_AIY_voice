import pandas as pd
import numpy as np
import zipfile
import subprocess
import matplotlib.pyplot as plt
from unicodedata import normalize

base_url = "https://schedules.calpoly.edu/subject" # get majority of class data
descrip_url = "https://schedules.calpoly.edu/courses" # get class names(description)
quarters = {'F':'curr', 'W':'next', 'S':'2224'}
subjects = ['AERO', 'BMED', 'CE', 'CPE', 'CSC', 'EE', 'ENGR', 'ENVE', 'IME', 'MATE', 'ME']

def filter_course(x):
    # removes trailing substrings with '/', '+'
    # "CPE 101 /1" -> "CPE 101"
    # I think NaN is treated as floaT? but this makes it work
    if type(x) is float:
        
        return
    
    items = x.split()
    if len(items) > 2:
        # Just removing third substring if its the
        return " ".join(items[:-1])
    else: return x
    
big_df = pd.DataFrame()
for q in quarters.keys():
    # add stuff to this empty df
    quarter_df = pd.DataFrame()
    q_val = quarters[q]
    for s in subjects:
        print(f'Fetching {base_url}_{s}_{q_val}.htm')
        # fetch html table that contains descrip for each class
        descrip_df = pd.read_html(f'{descrip_url}_{s}_{q_val}.htm', flavor='html5lib')[0] # fetch descrip
        # group together rows with same 'Course' val
        descrip_df.groupby(['Course']).agg({'Description':lambda x: x})
        
        # fetch html table with everything else
        subject_df = pd.read_html(f'{base_url}_{s}_{q_val}.htm', flavor='html5lib')[0]
        # Change erroneous classes with weird substrings to normal names
        subject_df['Course'] = subject_df['Course'].apply(filter_course)
        # merge two dfs based on Course name
        subject_df = subject_df.merge(descrip_df, on='Course')
        quarter_df = pd.concat([quarter_df, subject_df])
    quarter_df['Quarter'] = q
    big_df = pd.concat([big_df, quarter_df])
print(big_df.head())