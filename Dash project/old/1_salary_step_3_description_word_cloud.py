# Import pandas, numpy, plotly, regex, matplotlib, seaborn
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import re
import sys, os
from bs4 import BeautifulSoup
import string

# print( os.getcwd())
os.chdir("D:\\2_R_repo\\2_python repo\\Dash project")
dir_path = os.getcwd()
# print (job_counter)

# RESET data
df_merged = pd.read_csv(dir_path + "\\" + "merged_data.csv")
df_merged = df_merged.drop(['Unnamed: 0'], axis=1)
df_merged.convert_dtypes()
df_merged.fillna(axis=0, inplace=True, value="unknown", method=None)
df_merged = df_merged.applymap(lambda x: x.lower())

description_list = df_merged['description']
description_no_html_list = []

# remove HTML tags from text
for i in range(0, len(description_list)):
    html_str = description_list[i]
    soup = BeautifulSoup(html_str, features="html.parser")
    description_no_html_list.append(soup.get_text())

dict_words = {}
for i in range(0, 3):  # len(description_no_html_list)):
    use_this_string = description_no_html_list[i].translate(
        str.maketrans('', '', string.punctuation))
    words = use_this_string.split()
    print(words)
    for word in words:
        print(word)
        if word not in dict_words.keys():
            dict_words[word] = 1
        else:
            dict_words[word] += 1

print(dict_words)

# write result to text file
# with open('merged_df_description.txt', 'w', encoding='utf-8') as f:
#     f.writelines(description_no_html_list)
# f.close()
