# Import pandas, numpy, plotly, regex, matplotlib, seaborn
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import re
import json
import sys, os

# print( os.getcwd())
os.chdir("D:\\2_R_repo\\2_python repo\\Dash project")
dir_path = os.getcwd()
# print (job_counter)

# Load data, read.csv()
# Added Data: Country abbreviation list
# Added Data: State Abbreviations or short_names
df_flexjobs = pd.read_csv("flexjobs.csv")
df_indeed = pd.read_csv("indeed_jobs.csv")
df_simplyhired = pd.read_csv("simplyhired.csv")
df_countries = pd.read_csv("list_countries.csv", encoding='latin-1')
df_state_short_names = pd.read_csv("state_short_names.csv")

# Load data, json.loads()
# load data using Python JSON module
# file_path = 'dice.json'
with open('dice.json', 'r') as f:
    data = json.loads(f.read())

# extract json data to df
df_dice_json = pd.json_normalize(data, record_path=['data'])
df_dice_json_2 = pd.DataFrame(df_dice_json[
                                  ['title', 'companyName', 'summary', 'jobLocation.displayName',
                                   'salary', 'isRemote']])

# 1_cleaning data, json
df_dice_json_2['jobtype'] = np.where(df_dice_json_2['isRemote'] == True, 'remote', 'NA')
df_dice_json_2 = df_dice_json_2.drop(['isRemote'], axis=1)
new_column_names_list = ['title', 'company', 'description', 'location', 'salary', 'jobtype']
df_dice_json_2.columns = new_column_names_list

# 1_cleaning data, State list
state_short_name_list = df_state_short_names['short_name'].str.lower()
state_long_name_list = df_state_short_names['state_name'].str.lower()

# 1_cleaning data, Country list
country_short_name_list = df_countries['country'].str.lower()
country_long_name_list = df_countries['name'].str.lower()

# Merge data
df_rows_all = pd.concat([df_flexjobs, df_indeed, df_simplyhired, df_dice_json_2])
# print(df_rows_all.info())

# 1_cleaning data, merged data
df_rows_all = df_rows_all.drop(['Unnamed: 0'], axis=1)

# Export Data
df_rows_all.to_csv(dir_path + "\\" + "merged_data.csv")
