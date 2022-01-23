# Import pandas, numpy, plotly, regex, matplotlib, seaborn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sys, os
#print( os.getcwd())
os.chdir("D:\\2_R_repo\\2_python repo\\Dash project")
dir_path = os.getcwd()
#print (job_counter)

#RESET data
df_merged = pd.read_csv(dir_path + "\\" + "merged_data.csv")
df_merged = df_merged.drop(['Unnamed: 0'], axis = 1)
df_merged.convert_dtypes()
df_merged.fillna(axis=0, inplace=True,value="unknown", method=None)
df_merged['title'] = df_merged['title'].str.lower()
df_merged['salary'] = df_merged['salary'].str.lower()
df_merged['jobtype'] = df_merged['jobtype'].str.lower()
df_merged['location'] = df_merged['location'].str.lower()
df_merged['description'] = df_merged['description'].str.lower()
df_merged['company'] = df_merged['company'].str.lower()

# Jobtype Column
# process rows based on condition
df_merged = np.select(condlist=[df_merged['jobtype'].str.find("data scientist") > -1,
                                            df_merged['title'].str.find("data analyst") > -1,
                                            df_merged['title'].str.find("data engineer") > -1,
                                           ],
                                  choicelist=["data_scientist","data_analyst","data_engineer"],
                                  default=0)

df_merged = df_merged[(df_merged['jobtype'] != "flexible schedule job")]
df_merged = df_merged[(df_merged['jobtype'] != "temporary job")]
df_merged = df_merged[(df_merged['jobtype'] != "freelance job")]
df_merged = df_merged[(df_merged['jobtype'] != "part-time")]
df_merged = df_merged[(df_merged['jobtype'] != "full-time")]

#print( "new length= {}".format( len(df_merged['jobtype']) ) )

#print(df_merged['jobtype'].value_counts() )

"""Categorical variables created"""

df_merged['is_fully_remote'] = 0
#1-full remote, 0-not_remote
df_merged['is_fully_remote'] = np.select(condlist=[df_merged['jobtype'] == "100% remote job",
                                            df_merged['jobtype'] == "remote",
                                            df_merged['jobtype'] == "option for remote job",
                                            df_merged['jobtype'] == "partial remote job",
                                            df_merged['jobtype'] == "remote - during pandemic job"
                                           ],
                                  choicelist=[1,1,0,0,0], 
                                  default=0)
#df_merged['is_fully_remote'].value_counts(normalize=True, dropna=False)

"""Categorical variables created"""

df_merged['is_partial_remote'] = 0
#1-full remote, 0-not_remote
df_merged['is_partial_remote'] = np.select(condlist=[df_merged['jobtype'] == "100% remote job",
                                            df_merged['jobtype'] == "remote",
                                            df_merged['jobtype'] == "option for remote job",
                                            df_merged['jobtype'] == "partial remote job",
                                            df_merged['jobtype'] == "remote - during pandemic job"
                                           ],
                                  choicelist=[0,0,1,1,1], 
                                  default=0)
#df_merged['is_partial_remote'].value_counts(normalize=True, dropna=False)

"""Use Keywords to create new feature columns"""

df_merged['has_science'] = np.where ( df_merged['title'].str.find("science") > -1, 1,0 )
df_merged['has_scientist'] = np.where ( df_merged['title'].str.find("scientist") > -1, 1,0 )
df_merged['has_analyst'] = np.where ( df_merged['title'].str.find("analyst") > -1, 1,0 )
df_merged['has_engineer'] = np.where ( df_merged['title'].str.find("engineer") > -1, 1,0 )

df_merged['has_senior'] = np.where ( df_merged['title'].str.find("senior") > -1, 1,0 )
df_merged['has_director'] = np.where ( df_merged['title'].str.find("director") > -1, 1,0 )
df_merged['has_analytics'] = np.where ( df_merged['title'].str.find("analytics") > -1, 1,0 )

df_merged['has_data_science'] = np.where ( df_merged['title'].str.find("data science") > -1, 1,0 )
df_merged['has_data_scientist'] = np.where ( df_merged['title'].str.find("data scientist") > -1, 1,0 )
df_merged['has_data_analyst'] = np.where ( df_merged['title'].str.find("data analyst") > -1, 1,0 )
df_merged['has_data_engineer'] = np.where ( df_merged['title'].str.find("data engineer") > -1, 1,0 )

# initialize column
df_merged['remote_full_partial'] = "check"
#df.loc[df[‘column’] condition, ‘new column name’] = ‘value if condition is met’
df_merged.loc[ df_merged["is_fully_remote"] ==1, 'remote_full_partial'] = "remote_full"
df_merged.loc[ df_merged["is_partial_remote"] ==1, 'remote_full_partial'] = "remote_partial"
df_merged["remote_full_partial"].value_counts(normalize=True, dropna=False)

print( df_merged['is_fully_remote'].value_counts(normalize=True, dropna=False) )
print( df_merged['is_partial_remote'].value_counts(normalize=True, dropna=False) )

"""# Salary column

## 1_Cleaning data
"""

df_merged['salary'] = df_merged['salary'].str.replace(',', '')

"""### REGEX reset

## 1_Cleaning data
regex, regular expressions
"""

regex_results_1 = df_merged['salary'].str.extract(r'(?P<sal_1>\$\d\w+)', expand=True)

regex_results_2 = df_merged['salary'].str.extract(r'(?P<sal_1>\$\d\w+\W-\s\$\d\w+\s)', expand=True)

"""## 1_Cleaning data
Remove "$"-sign
"""

# single number salary
regex_results_1['sal_1'] = regex_results_1['sal_1'].str.replace("$","").str.lstrip()
# range of min-max salary
regex_results_2['sal_1'] = regex_results_2['sal_1'].str.replace("$","").str.lstrip()

"""## 1_Cleaning data
Split using separator "-"
"""

regex_results_3 = regex_results_2['sal_1'].str.split("-", n = 1, expand = True)

"""Remove "$"-sign"""

regex_results_3['sal_min'] = regex_results_3[0].str.replace("$","").str.lstrip()
regex_results_3['sal_max'] = regex_results_3[1].str.replace("$","").str.lstrip()

"""Add back split min_max values to source df"""

regex_results_2['sal_min'] = regex_results_3['sal_min']
regex_results_2['sal_max'] = regex_results_3['sal_max']

"""## 1_Cleaning data
Drop column containing redundant information 
"""

regex_results_2.drop('sal_1', axis=1, inplace=True)

"""## 1_Cleaning data
Replace NaN with 0 to enable error-free aritmetic operations
"""

regex_results_2.fillna(0, inplace=True)

regex_results_2['sal_min'] = regex_results_2['sal_min'].astype(int)
regex_results_2['sal_max'] = regex_results_2['sal_max'].astype(int)

"""## 1_Cleaning data
Consolidate Salary data. 
1.   if only 1 number available use it as min and max. 
2.   if range available then use separate min and max.
3.   convert data types to appropriate ones





"""

# convert data types
regex_results_1['sal_1'] = regex_results_1['sal_1'].astype(float)
# fill na with 0
regex_results_1.fillna(0, inplace=True)
# convert data types
regex_results_1['sal_1'] = regex_results_1['sal_1'].astype(int)
# consolidate data
regex_results_2['sal_1'] = regex_results_1['sal_1']

# if only 1 number available use it as min and max. 
regex_results_2.loc[regex_results_2['sal_min'] ==0,'sal_min'] = regex_results_2['sal_1']
regex_results_2.loc[regex_results_2['sal_max'] ==0,'sal_max'] = regex_results_2['sal_1']
regex_results_2.drop('sal_1', axis=1, inplace=True)

# if only 1 number available use it as min and max. 
df_merged['sal_max'] = regex_results_2['sal_max']
df_merged['sal_min'] = regex_results_2['sal_min']

"""## 1_Cleaning data
Update salary monthly multiplier
"""

# regex_results_4 = pd.DataFrame( df_merged['salary'].str.contains('month') )
# #regex_results_4
# salary_is_monthly_list = regex_results_4.index[regex_results_4['salary'] == True].tolist()
# #print(salary_is_monthly_list)
# #print(len(salary_is_monthly_list))
# #df_merged.iloc[salary_is_monthly_list,]
# df_merged['monthly_multiplier'] = 0
# df_merged['monthly_multiplier'].loc[salary_is_monthly_list,] = 12
# #df_merged['monthly_multiplier'].value_counts()

"""Update salary hourly multiplier"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# regex_results_5 = pd.DataFrame( df_merged['salary'].str.contains('hour') )
# #regex_results_5
# salary_is_hourly_list = regex_results_5.index[regex_results_5['salary'] == True].tolist()
# #print(salary_is_hourly_list)
# #print(len(salary_is_hourly_list))
# #df_merged.iloc[salary_is_hourly_list,]
# df_merged['hourly_multiplier'] = 0
# df_merged['hourly_multiplier'].loc[salary_is_hourly_list,] = 2000
# #df_merged['hourly_multiplier'].value_counts()

"""Update salary yearly multiplier"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# regex_results_6 = pd.DataFrame( df_merged['salary'].str.contains('year') )
# #regex_results_6
# salary_is_yearly_list = regex_results_6.index[regex_results_6['salary'] == True].tolist()
# #print(salary_is_yearly_list)
# #print(len(salary_is_yearly_list))
# #df_merged.iloc[salary_is_yearly_list,]
# df_merged['yearly_multiplier'] = 0
# df_merged['yearly_multiplier'].loc[salary_is_yearly_list,] = 1
# #df_merged['yearly_multiplier'].value_counts()

df_merged['sal_global_multiplier'] = df_merged['hourly_multiplier'] + df_merged['monthly_multiplier'] + df_merged['yearly_multiplier']

df_merged['sal_max_yearly'] = df_merged['sal_max'] * df_merged['sal_global_multiplier']
df_merged['sal_min_yearly'] = df_merged['sal_min'] * df_merged['sal_global_multiplier']

"""# Location Column

## Reset location
"""

df_location = df_merged['location']

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# remove_this = re.compile(r'\w+,[[:space:]]\w+')
# regex_results_new = df_location.str.replace(remove_this, "")

"""RESET split_location"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# split_location = regex_results_new.str.split(",", n = 2, expand = True)
# split_location.columns = ["city","state_short","country"]
# split_location['city'] = split_location['city'].str.strip().str.lower()
# split_location['state_short'] = split_location['state_short'].str.strip().str.lower()
# # drop column, country
# split_location = split_location.drop('country' , axis='columns')
# # fillna
# split_location.fillna(axis=0, inplace=True,value="unknown", method=None)

"""Extract state short name"""

# %%capture
split_location['len_state_short'] = 0
split_location['state_short_clean'] = "xx"

for index_1 in range(0, len(split_location)):
  split_location['len_state_short'][index_1] = len(split_location['state_short'][index_1])

  if (split_location['len_state_short'][index_1] >= 2):
    split_location['state_short_clean'][index_1] = split_location['state_short'][index_1][0:2]

  else:
    split_location['state_short_clean'][index_1] = "unknown"
  #if split_location['state_short']
  #print(index_1,"=index ",",,item=", split_location['state_short'][index_1])

"""Replace some values"""

split_location['city_clean'] = np.where(split_location['city'] == "us national", "remote", split_location['city'] )
split_location['city_clean'] = np.where (split_location['city_clean'].str.contains('remote'), "remote", split_location['city_clean'] )

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# remove_char_string = "~!@#$%^&*()_-+=\[]{}:;,<>?/"
# split_location['city_clean_2'] = split_location['city_clean']
# 
# for index_1 in range(0, len(split_location['city_clean'])):
#   word = split_location['city_clean'][index_1]
#   for i in range(0, len(word)):
#     char_1 = word[i]
#     if char_1 in remove_char_string:
#       word_2 = word.replace(char_1,"__").split("__")[0]
#       split_location['city_clean_2'][index_1] = word_2        
# 
# # print(split_location['city_clean_2'].unique())

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# remove_char_string = "\xa0"
# split_location['city_clean_3'] = split_location['city_clean_2']
# 
# for index_1 in range(0, len(split_location['city_clean_2'])):
#   word = split_location['city_clean_2'][index_1]
#   for i in range(0, len(word)):
#     char_1 = word[i]
#     if char_1 in remove_char_string:
#       word_2 = word.replace(char_1,"__").split("__")[0]
#       split_location['city_clean_3'][index_1] = word_2
# 
# #print(split_location['city_clean_3'].unique())

# copy column as default
split_location['city_clean_4'] = split_location['city_clean_3']

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# for index_1 in range(0, len(split_location['city_clean_3'])): 
#   word = split_location['city_clean_3'][index_1]
#   #print("input word=", word)
# 
#   if word in country_long_name_list.unique():
#     split_location['city_clean_4'][index_1] = "unknown"
#     #print("index=", index_1, "    country_long= ", word, " replaced with=", split_location['city_clean_4'][index_1] )
#  
#   elif word in state_short_name_list.unique():
#     split_location['city_clean_4'][index_1] = "unknown"
#     #print("index=", index_1, "         state_short= ", word, "  replaced with=", split_location['city_clean_4'][index_1] )
# 
#   elif word in state_long_name_list.unique():
#     split_location['city_clean_4'][index_1] = "unknown"
#     #print("index=", index_1, "             state_long= ", word, "   replaced with=", split_location['city_clean_4'][index_1])
#   
#   #print( split_location['city_clean_4'].unique() )

"""## 1_Cleaning data
cleanup state short names
"""

split_location['state_short_clean_2'] = split_location['state_short_clean']

for index_1 in range(0, len(split_location['state_short_clean'])): 
  word = split_location['state_short_clean'][index_1]
  #print("input word=", word)

  if word not in state_short_name_list.unique():
    split_location['state_short_clean_2'][index_1] = "unknown"
    #print("index=", index_1, "    state_short_clean= ", word, " replaced with=", split_location['state_short_clean_2'][index_1] )

"""## Add back clean location data"""

# add cleaned, preprocessed columns
df_merged['state_short_clean_2'] = split_location['state_short_clean_2']
df_merged['city_clean_4'] = split_location['city_clean_4']

"""## Cleaning done, Location

# RESTART RUNTIME IF PLOTLY BREAKS.
DO NOT FACTORY RESET RUNTIME. IF DONE, THEN RE-ENTER G_DRIVE CREDENTIALS TO REMOUNT.
THEN RUN ALL ABOVE AGAIN. THEN RUN BELOW CELLS.

# USING PLOTLY
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# %pip install --upgrade plotly

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# %pip install --upgrade plotly express

import plotly.express as px
import plotly.graph_objects as go

"""Get clean copy of data"""

df_merged.columns

df_merged_clean = df_merged[ ['title', 'jobtype', 'company','sal_max_yearly',
                            'sal_min_yearly','state_short_clean','city_clean',
                            'is_fully_remote','is_partial_remote',
                            'has_science', 
                            'has_scientist', 'has_analyst', 'has_engineer', 
                            'has_senior', 'has_director', 
                            'has_analytics','has_data_science', 
                            'has_data_scientist', 'has_data_analyst', 'has_data_engineer'] 
                            ]

is_remote_col_names = ['is_fully_remote', 'is_partial_remote']
has_job_keywords_col_names = ['has_data_analyst','has_data_scientist','has_data_engineer','has_data_science']

# using plotly express
fig = px.bar(title= "job title VS is_fully_remote", 
       data_frame= df_merged_clean, 
       y= 'is_fully_remote', 
       x= has_job_keywords_col_names,
       barmode= 'group',
       opacity= 1, 
       facet_col = 'is_fully_remote'
       )

fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)'#,
#'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig.show()

# using plotly express
fig = px.bar(title= "job title VS is_partial_remote", 
       data_frame= df_merged_clean, 
       y= 'is_partial_remote', 
       x= 'city_clean',
       #barmode= 'group',
       opacity= 1, 
       #facet_col = 'is_partial_remote',
       hover_data=has_job_keywords_col_names
       )

fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)'#,
#'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig.show()

df_merged_clean.info()

df_merged_clean_subset = df_merged_clean[['sal_max_yearly',
                            'sal_min_yearly',
                            'is_fully_remote','is_partial_remote',
                            'has_analytics','has_data_science', 
                            'has_data_scientist', 'has_data_analyst', 'has_data_engineer']]

df_salary_grouped = df_merged_clean_subset.groupby(by='is_fully_remote')

df_salary_grouped.head()

"""# JUPYTER_DASH_APP"""

# JUPYTER_DASH
# create app
app_salary = JupyterDash(__name__)

# create layout for app
app_salary.layout = html.Div(children=[
    html.H1(children='dashboard_for_salary'),
    dcc.Dropdown(id='company_dropdown',
                 options=[{'label': i, 'value': i} 
                          for i in df_merged_clean['company'].unique()],
                 value='unknown'),
    dcc.Graph(id='company_graph')
])

# Define callback to update graph
@app_salary.callback(
    Output(component_id='company_graph', component_property='figure'),
    Input(component_id='company_dropdown', component_property='value')
)
def update_graph(selected_company):
    filtered_df_merged = df_merged_clean[ df_merged_clean['company'] == selected_company ]
    
    bar_fig = px.bar(title= f'{selected_company}, company; job title VS is_fully_remote', 
                    data_frame= filtered_df_merged, 
                    y= 'salary', 
                    x= has_job_keywords_col_names,
                    barmode= 'group',
                    opacity= 1, 
                    facet_col = 'is_fully_remote'
                    )

    bar_fig.update_layout( { 'plot_bgcolor': 'rgba(0, 0, 0, 0)' } )

    bar_fig.show()

    return bar_fig
    
# Run app and display result inline in the notebook
if __name__ == '__main__':
    app_salary.run_server(debug=True, mode= 'external') #'inline')

"""# Non-Dash, Pie-Chart"""

# NON-DASH
# define func to make pie-chart
def draw_pie_chart(label_have):
  labels = 'have', '_not'
  colors = ['g', 'y']

  data_labels = [ df_merged_clean[str(label_have)].value_counts(normalize=True)[1], 
           df_merged_clean[str(label_have)].value_counts(normalize=True)[0]
         ]
  explode = (0.1, 0)
  plt.pie(data_labels, 
          labels=labels, 
          colors=colors, 
          explode=explode, 
          startangle=90, 
          shadow=True, 
          autopct='%1.1f%%')
  plot_title = 'job title has keywords ' + str(label_have)[4:]
  plt.title(plot_title)
  plt.show()

#call func
#draw_pie_chart("has_science")

#call func
#draw_pie_chart("has_scientist")

#call func
#draw_pie_chart("has_analyst")

#call func
#draw_pie_chart("has_scientist")

#call func
#draw_pie_chart("has_engineer")

#call func
draw_pie_chart("has_data_scientist")

"""### Explain Pie-chart
almost 20% of job titles have data_scientist keyword.
"""

#call func
draw_pie_chart("has_data_analyst")

"""### Explain Pie-chart
only 8% (rounded up) of job titles have data_analyst keyword.
"""

#call func
draw_pie_chart("has_data_engineer")

"""### Explain Pie-chart
only 4% (rounded up) of job titles have data_engineer keyword.
"""

df_title_category = pd.DataFrame(df_merged_clean.has_science.value_counts(dropna=False) )
df_title_category.rename(columns={"has_science":"frequency"}, inplace=True)
df_title_category.reset_index(inplace=True, drop=False) 
df_title_category.rename(columns={"index":"has_science"}, inplace=True)

df_title_category.plot(figsize=(12,10),kind='bar', 
                  x='has_science', 
                  y='frequency', 
                  ylabel="frequency",
                  title="Histogram of has_science observations")\
          .set_xticklabels(rotation=90,labels=df_title_category['has_science'])

"""### Explain histogram, has_science
majority of the job title do NOT contain keyword "science"
"""

df_title_category = pd.DataFrame(df_merged_clean.has_analyst.value_counts(dropna=False) )
df_title_category.rename(columns={"has_analyst":"frequency"}, inplace=True)
df_title_category.reset_index(inplace=True, drop=False) 
df_title_category.rename(columns={"index":"has_analyst"}, inplace=True)

df_title_category.plot(figsize=(12,10),kind='bar', 
                  x='has_analyst', 
                  y='frequency', 
                  ylabel="frequency",
                  title="Histogram of has_analyst observations")\
          .set_xticklabels(rotation=90,labels=df_title_category['has_analyst'])

"""### Explain histogram, has_analyst
majority of the job title do NOT contain keyword "analyst"
"""

df_title_category = pd.DataFrame(df_merged_clean.has_engineer.value_counts(dropna=False) )
df_title_category.rename(columns={"has_engineer":"frequency"}, inplace=True)
df_title_category.reset_index(inplace=True, drop=False) 
df_title_category.rename(columns={"index":"has_engineer"}, inplace=True)

df_title_category.plot(figsize=(12,10),kind='bar', 
                  x='has_engineer', 
                  y='frequency', 
                  ylabel="frequency",
                  title="Histogram of has_engineer observations")\
          .set_xticklabels(rotation=90,labels=df_title_category['has_engineer'])

"""### Explain histogram, has_engineer
majority of the job title do NOT contain keyword "engineer"
"""

has_job_keywords_col_names = ['has_data_analyst','has_data_scientist','has_data_engineer']
col_sums_1 = df_merged[has_job_keywords_col_names].sum()
col_sums_2 = col_sums_1.sum()
a = int( round( 100*( col_sums_2 / len(df_merged['title'])),2))
print("only {}% jobtitles have either of these keywords 'data_analyst','data_scientist','data_engineer'.".format(a))

b=  round( 100*( col_sums_1 / len(df_merged['title'])),0)
#print (b)
print("only {}% jobtitles have either of these keywords 'data_scientist'.".format( int( b[1] ) ) )
print("only {}% jobtitles have either of these keywords 'data_analyst'.".format( int( b[0] ) ) )
print("only {}% jobtitles have either of these keywords 'data_engineer'.".format( int( b[2] ) ) )

"""# Correlations"""

df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly', 'is_fully_remote', 'is_partial_remote']]
corr_1 = df_merged_clean_subset.corr() # get correlation object
corr_1

"""## Maximum Salary


* Maximum yearly salary is neagtively correlated with jobtype being fully or 
partially remote.
* Maximum yearly salary is highly correlated with minimum yearly salary.


"""

df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly',
                                          'has_scientist', 'has_analyst', 'has_engineer',
                                          'has_data_scientist', 'has_data_analyst','has_data_engineer']]

corr_2 = df_merged_clean_subset.corr() # get correlation object
corr_2

"""## salary, job title keywords


* Maximum yearly salary is positively correlated with titles that have "analyst" keyword. 
Surprisingly "data_analyst" keyword has job_counter weaker coorelation as compared to "analyst". 
This suggests more specialist job titles tend to offer lower maximum yearly salary.
"""

df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly',
                                          'has_senior', 'has_director']]

corr_3 = df_merged_clean_subset.corr() # get correlation object
corr_3

"""## salary, job seniority keywords


* Maximum yearly salary is negatively correlated with titles that have "Director" keyword. 
This is not very surprising since you expect salary to be only job_counter subset of total compensation. 

"""

df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly',
                                          'has_science', 'has_scientist', 
                                          'has_analytics',
                                          'has_data_science']]

corr_4 = df_merged_clean_subset.corr() # get correlation object
corr_4

"""* Maximum yearly salary is negatively correlated with titles that have "scientist" keyword.

## [22] sns.heatmap()
"""

df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly',
                                          'is_fully_remote', 'is_partial_remote', 
                                          'has_science', 'has_scientist', 
                                          'has_analyst','has_engineer', 
                                          'has_senior', 'has_director', 
                                          'has_analytics', 'has_data_science', 
                                          'has_data_scientist', 'has_data_analyst',
                                          'has_data_engineer']]

corr_5 = df_merged_clean_subset.corr() # get correlation object
#corr_5

ax = sns.heatmap( corr_5, 
                  vmin=-1, vmax=1, center=0,
                  cmap=sns.diverging_palette(100, 520, n=100),
                  square=True
                )

ax.set_xticklabels(
                    ax.get_xticklabels(),
                    rotation=45,
                    horizontalalignment='right'
                  )

"""### Explain Heatmap
* Maximum yearly salary shows strongest correlation with job titles with keywords "analyst" and "data_analyst". Also it is job_counter positive correlation.
"""

df_merged_clean.columns

df_merged_clean['state_short_clean'].value_counts()

# create filtered df for grouping
df_merged_clean_subset = df_merged_clean[['sal_max_yearly', 'sal_min_yearly','state_short_clean']]
df_merged_clean_subset = df_merged_clean_subset [ df_merged_clean_subset['state_short_clean']!= "un" ]
df_merged_clean_subset['state_short_clean'].value_counts()[0:30]

# get median salary_max data by city
groupby_column_name = "state_short_clean"
median_df_grouped_salary_max = pd.DataFrame(df_merged_clean_subset.groupby(groupby_column_name)['sal_max_yearly'].agg('median'))
# sort values of median(salary_max), descending order
median_df_grouped_salary_max.sort_values(by='sal_max_yearly',ascending=False,inplace=True)
median_df_grouped_salary_max.reset_index(inplace=True, drop=False)
#plot
plt.figure(figsize=(20, 6))

f = median_df_grouped_salary_max['sal_max_yearly'].plot( 
        kind='bar', 
        title="bar plot median(salary_max)", 
        xlabel= groupby_column_name)

f.set_xticklabels(rotation= 90,
                   labels= median_df_grouped_salary_max[groupby_column_name])
plt.ylabel('median(salary_max)')

display(f)





"""### Explain barplot

Per above plot, in general, covid19 data generally decreases with age_group. that is lower age tends to result in lower covid19 data. covid19 data is euphemism for covid19 deaths.
"""

# get sum of covid19 data by age_group, Sex
df_4 = pd.DataFrame(pandas_df.groupby(['age_group','sex'])['covid_19'].sum().reset_index())
df_4.sort_values(by=['covid_19'],ascending=True,inplace=True)
df_4.reset_index(inplace=True, drop=True)
print(df_4, "\n", type(df_4))

df_4.boxplot('covid_19','age_group',rot = 90,figsize=(10,6))

"""#### Explain Boxplot

Per the boxplot above, maximum COVID19 data seems to belong to age_group (80+ years). 
age_group <18years, has the lowest COVID19 data.
"""

#type(df_4)
df_4.info()

df_4['sex'] = df_4['sex'].astype('category')
df_4['sex'].describe()

plot_male = df_4[df_4['sex']=="Male (M)"].plot(kind='bar',
          x="age_group", 
          y='covid_19', 
          figsize=(4,5), 
          ylabel='COVID19_data', 
          title="bar plot of COVID19 vs age_group")

plot_female = df_4[df_4['sex']=="Female (F)"].plot(kind='bar',
          x="age_group", 
          y='covid_19', 
          figsize=(4,5), 
          ylabel='COVID19_data', 
          title="bar plot of COVID19 vs age_group")

df_5 = df_4.groupby(['age_group', 'sex'])['covid_19'].agg('sum').unstack('age_group').fillna(0)
#df_5.plot(kind='bar', stacked=True)

df_5.head()

df_5.describe()

df_5.shape

df_5.plot(kind="bar")

"""Explain barplot
the covid_19 for sex=Female is higher than sex=Male, in 80+ age_group.
Fo other age_groups, generally covid_19 for sex=Female is lower than sex=Male.

# Advanatges of pyspark over pandas


1.   PySpark is very fast. per some sources, it is 100x faster than pandas.

2.   PySpark uses distributed computing. So local-resources do not really to scale with data_frame size. So suitable for big-data. So pysaprk acan "scale" with data-sizes.
In Pandas, the data_frame size that can be handled is limited by local-Resources. Plus pandas do not use parallel or distributed computing. So pandas cannot really "scale" with data-size.


3.   PySpark is very fast, in part because it is not really running python in the background. So using apache spark builtin functions are critical to achieving the lightining fast speeds. 
Pandas on the other hand execute python code for the most part, so comparitively slower.

4. PySpark uses lazy execution, so does NOT execute immediately unless (show()) or other collect() type code is reached.
Pandas executes immediately regardless of whether show() or equivalent code is reached.
"""