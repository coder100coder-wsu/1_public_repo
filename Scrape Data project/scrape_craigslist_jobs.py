import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas

# declare empty dictionary
dict_jobs = {}
job_counter = 0
# specify target  or root or seed webpage url
# url = "https://boston.craigslist.org/search/sof"
url = "https://boston.craigslist.org/search/etc"
############################################
# loop to crawl all linked pages, until "next page" is NOT available
while True:
    response = requests.get(url)  # expected response 200. error is 404.
    #print(response)
    data = response.text  # extract text from response to "requests"
    # if file exists, append data
    # if file does NOT exist, python creates the file
    # file path is located in working directory
    # with open('save_web_response.txt', 'a+') as f:
    #     f.write(data + "\n")  # insert next line character
    #     # lines = f.read()  # read the file if storing and reading are separate steps
    # "with open" automatically closes file. no need for explicit "file.close()".
    ############################################
    # parse html using BeautifulSoup
    # soup = BeautifulSoup(lines, 'html.parser')
    soup = BeautifulSoup(data, 'html.parser')
    # print(soup)
    ############################################
    # specify "wrapper" class, from inspection of webpage, in some web browser
    jobs = soup.find_all('div', {"class": "result-info"})
    # print(jobs[1])
    # loop through all items of object "jobs"
    for job in jobs:
        # print(job)
        # specify individual class or html tags, from inspection of webpage, in some web browser
        # extract text without html tags
        # add condition, if result is NoneType, add text "NA" instead of failing or traceback
        title = job.find('a', {"class": "result-title"}).text \
            if job.find('a', {"class": "result-title"}).text \
            else "NA"
        # string slicing based on observation of results
        location = job.find('span', {"class": "result-hood"}).text[2:-1] \
            if job.find('span', {"class": "result-hood"}).text[2:-1] \
            else "NA"
        date = job.find('time', {"class": "result-date"}).text \
            if job.find('time', {"class": "result-date"}).text \
            else "NA"
        link = job.find('a', {"class": "result-title"}).get('href') \
            if job.find('a', {"class": "result-title"}).get('href') \
            else "NA"
        # get link for job description, go to hyperlinked webpage, parse html
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data, 'html.parser')
        # specify individual class or html tags, from inspection of webpage, in some web browser
        # extract text without html tags
        # add condition, if result is NoneType, add text "NA" instead of failing or traceback
        job_description = job_soup.find('section', {'id': 'postingbody'}).text \
            if job_soup.find('section', {'id': 'postingbody'}).text \
            else "NA"
        # job attributes, salary etc
        job_attributes = job_soup.find('p', {'class': 'attrgroup'}).text \
            if job_soup.find('p', {'class': 'attrgroup'}).text \
            else "NA"
        # update job counter
        job_counter += 1
        # update dict[key] = value
        dict_jobs[job_counter] = [title, job_attributes, location, date, link,job_description]
        # print(" title_{}_\n location_{}_\n date_{}_\nlink_{}_\n description_{}_\n attributes_{}_".
        #       format(title, location, date, link, job_description[50:100], job_attributes))
    # go to next webpage
    url_next_page = soup.find('a', {'title': 'next page'})
    # print("url_next_page={}".format(url_next_page))
    # break the while loop if no more hyperlinks to "next page", indicating last page
    if url_next_page.get('href'):
        url = 'https://boston.craigslist.org' + url_next_page.get('href')
        # print("url_next_page= {}".format(url_next_page))
    else:
        break
# print total no. of jobs
print("total jobs= {}".format(job_counter))
# store dict as dataframe
df_jobs = pd.DataFrame.from_dict(data=dict_jobs, orient='index',
                                 columns=['Title', 'Attributes', 'Location', 'Date', 'Link',
                                          'Description'])
# store results, write to csv
df_jobs.to_csv(path_or_buf='df_jobs.csv', index=False)
#print(df_jobs.info())
#print(df_jobs.head())
############################################
# address = soup.find_all("span", {"class": "result-hood"})
# #print(address)
# list_of_address = []
# for item in address:
#     list_of_address.append(item.text)
# print(list_of_address[0:10])
############################################
# tags = soup.find_all('job_counter')
# # print(tags)
# list_of_links = []
# for tag in tags:
#     list_of_links.append(tag.get('href'))
# # print(tag.get('href'))
# #print(list_of_links[0:10])
# ############################################
# titles = soup.find_all("job_counter", {"class": "result-title"})
# list_of_titles = []
# for title in titles:
#     list_of_titles.append(title.text)
# print(list_of_titles[0:10])
############################################

read_back_df_jobs = pd.read_csv('df_jobs.csv')
print( read_back_df_jobs.info())
print((read_back_df_jobs.head(5)))