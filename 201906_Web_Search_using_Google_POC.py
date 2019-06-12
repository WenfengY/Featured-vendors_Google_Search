# Project: Footprint Improvement Umbrella - Featured vendors 
#  - - Data driven leveraging Google Search API for strength of association - e.g. Netflix and AWS
# Goal: using Google Web Search Page # Results to verify that which service provider (SP) is the primary
#      one
# Idea: to find a way to automate the capture of whenever a vendor / technology organization features
# a user organization.
# Steps: 
# 1. identify standard customer pages on vendor (cloud service provider) companies' website to find
#     customers, and form a list of 126 for 6 vendors (AWS, Azura, Google Could, Oracle Cloud, IBM Cloud, 
#     Alibaba Cloud)
# 2. using Python Library selenium as major tool for headless web searching tool to search and parse 
#    the result pages, recoding search result # for 6 vendors
# 3. based on the #s for each customer, calculate the weights/percentages for all 6 vendors
#    and pick the top one as the major SP for comparison
# 4.  Verify our hypothesis: the google search result page #s represent the SP association levels


# Date: 201906
# Result: the searching results don't support our hypothesis

# No warnings displaying
import warnings
warnings.filterwarnings('ignore')

from selenium import webdriver
import os.path
import string
from bs4 import BeautifulSoup
import time
from random import random
import re
import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import requests

from datetime import datetime
startTime = datetime.now()

####################################################################################
# Function: purge_string
####################################################################################
# func: purge_string()
def purge_string(self, stop_words, special_chars=None, lower_case=False):
    val = self

    if lower_case:
        val = val.lower()

    # hardcoded separator
    val = val.replace(",", " ")

    # purge special characters
    if special_chars is not None:
        for char in special_chars:
            val = val.replace(char, '')

    # purge stopwords
    for char in stop_words:
        # Match beginning of name
        pattern = "^" + char + "\s(.*)"
        match = re.match(pattern, val)
        
        if match is not None:
            val = match.group(1)
        # Match standalone word
        pattern = "(.*)\s" + char + "\s(.*)"
        match = re.match(pattern, val)
        
        if match is not None:
            val = match.group(1) + " " +match.group(2)
        # Match end of name
        pattern = "(.*)\s+" + char + "$"
        match = re.match(pattern, val)
        
        if match is not None:
            val = match.group(1)
    
    # purge special characters
    if special_chars is not None:
        for char in special_chars:
            val = val.replace(char, '')
    
    # Strip white space
    val = val.strip()

    return val
####################################################################################
    
def randn():
    return(random())


def search_pages(company,vendor):
    url = 'https://www.google.com/search?q={}+{}'.format(company,vendor)    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(url)
    htmlSource = driver.page_source
    try:
        soup = BeautifulSoup(htmlSource, "html5lib")
        phrase_extract = soup.find(id="resultStats")
        val = int(phrase_extract.get_text().split(' ')[1].replace(',',''))
    except Exception as e:
        val = 0
    #chrome_options.quit()
    driver.close()
    driver.quit()
    return(val)


# Main part 

path = 'C:/Users/WenfengYan/Desktop/CC_201904/Project_Featured vendors_201904/'

company_list = pd.read_csv(path+'POC_list.csv', encoding = 'unicode_escape')



def refine_name (x):
    # Words to purge before applying matching algorithm
    purge_ls = ['"', "'s", "'", '.', '’', '...'         \
                , ',', '-', '+', '(', ')', '&', '#', '_', '/', '\\', '*', '‚', '”', '„', '*','?','!'] 
    # "', '".join(purge_ls)
    "; ".join(purge_ls)

    stopwords = \
    "incorporated|inc|corporation|corp|company|co|liability|limited" \
    "|ltd|jsc|ab|ag|saog|gmbh|lp|pjsc|psc|kpsc|ojsc|spa|tbk|pt|the" \
    "|and|partnership|private|services|a/s|as|s/a|sa|s.a.|pcl" \
    "|public company limited|plc|(publ)".split("|")
    # "', '".join(stopwords)

    return purge_string(x , stop_words=stopwords,
                   special_chars=purge_ls,
                   lower_case=True)

 
company_list['Company_Name'] = company_list['Customer'].apply(lambda x: refine_name(x))                



Cloud_Provider = ['AWS', 'Azura', 'Google Could', 'Oracle Cloud', 'IBM Cloud', 'Alibaba Cloud' ]
Cloud_Provider_S= ['AWS', 'Azura', '\"Google Cloud\"', '\"Oracle Cloud\"', '\"IBM Cloud\"', '\"Alibaba Cloud\"' ]


for i in Cloud_Provider:
    company_list[i] = 0
for i in Cloud_Provider:
    company_list[i+'_pct']=0

company_list['Service_Provider'] ='  '



for i in range(len(company_list)):
    company = company_list.loc[i]['Company_Name']
    for j in range(len(Cloud_Provider)):
        
        # wait time
        time.sleep(0.1)
        time.sleep(randn())
        
        k = search_pages(company, Cloud_Provider_S[j])
        company_list.at[i, Cloud_Provider[j]] = k
    if i//1 == i/1: 
    # if i == 3: 
        print( i+1 ,' out of ', len(company_list), ' are done! Current value is: ', k )
        print("TIME ELAPSED: ", (datetime.now() - startTime))


a = 0
b = 0
head_position = 4
for i in range(len(company_list)):
    a = company_list.loc[i][head_position:head_position+len(Cloud_Provider)].max()
    b = company_list.loc[i][head_position:head_position+len(Cloud_Provider)].sum()
    # print(a)
    if a == 0: 
        company_list.at[i,'Service_Provider'] = 'None'
        for k in Cloud_Provider:
            company_list.loc[i][k+'_pct']=0.00
    else:
        for j in Cloud_Provider:
            tmp = int(float((company_list.loc[i][j]*1.00) / b)*100)
            # print(tmp)
            company_list.at[i, j+'_pct']= tmp
            if company_list.loc[i][j] == a:
                company_list.at[i,'Service_Provider'] = j



cl = company_list.copy()

cl.head(10)