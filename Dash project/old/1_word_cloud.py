import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json

from wordcloud import WordCloud, STOPWORDS
import sys, os
os.chdir(sys.path[0])

# Load files and read text
#file_dir = "D:\\2_R_repo\\2_python repo\\Dash project\\Wordcloud_Tutorial"
text = open('merged_df_description.txt', mode='r', encoding='utf-8').read()
stopwords = STOPWORDS

wc = WordCloud(
        background_color='white',
        stopwords=stopwords,
        height = 600,
        width=400
)

wc.generate(text)

# store to file
wc.to_file('wordcloud_for_description.png')
