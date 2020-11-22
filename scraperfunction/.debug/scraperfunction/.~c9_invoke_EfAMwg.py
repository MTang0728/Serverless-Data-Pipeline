"""
scrape to DynamoDB
"""

import boto3
import json
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

import pandas as pd

DYNAMODB = boto3.resource('dynamodb')
TABLE = "deals"
PAGES = 1

#SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

def time_convert(time):
    '''
    convert scraped time to post time
    ---------------------------------
    input: scraped time in string
    output: post time in iso format in string
    '''
    current_time = datetime.now()
    if time == 'Just now':
        return current_time.isoformat(timespec='hours')
    if 'mins' in time:
        diff = timedelta(minutes = int(time[:-9]))
        return (current_time - diff).isoformat(timespec='hours')
    if 'hrs' in time:
        diff = timedelta(hours = int(time[:-8]))
        return (current_time - diff).isoformat(timespec='hours')
    if 'days' in time:
        diff = timedelta(days = int(time[:-9]))
        return (current_time - diff).isoformat(timespec='hours')

def name_clean(name):
    '''
    clean brandname
    ---------------------------------
    input: brandname in string
    output: cleaned brandname in string
    '''
    if name[-4:] == '.com':
        return name[:-4]
    elif name == 'COACH Outlet':
        return name[:5]
    else:
        return name

def fill_table(table_name, df):
    '''
    fill dynamoDB table
    -------------------
    input: dynamoDB table name in string
           cleaned scraped data in a dataframe
    '''
    LOG.info(f"filling Table {table_name}")
    table = DYNAMODB.Table(table_name)
    
    nrows = df.shape[0]
    for i in range(nrows):
        brand_name = df.iloc[i, 0]
        post_time = df.iloc[i, 1]
        comment_num = df.iloc[i, 2]
        like_num = df.iloc[i, 3]
        share_num = df.iloc[i, 4]
        LOG.info(f'adding {brand_name}')
        table.put_item(
            Item = {
                'brandname': brand_name,
                'posttime': post_time,
                'comment_num': comment_num,
                'like_num': like_num,
                'share_num': share_num
            }
            )

def scraper(table, pages):
    '''
    An automatic scraping function to scrape the newest posts on dealmoon.com website. 
    -----------------------------------------------------------------------------------
    input: number of pages
    Output: A csv file. 
    '''
    
    # create a dataframe for storing the result
    result = pd.DataFrame(columns=('brandname', 'time', 'comment_num', 'like_num', 'share_num'))
    hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
    
    for page in range(pages):
        url = 'https://www.dealmoon.com/en?p=%d' %(page)
        req = urllib.request.Request(url, headers=hdr)
        response = urlopen(req)
        soup = BeautifulSoup(response.read(), 'html.parser')

        for article in soup.find_all('div', class_ = "right-cnt"):
            try:
                # get brand name
                brandname = article.find('a', class_ = 'ib ib-store j-store').text
                brandname = name_clean(brandname)
                # get time
                time = article.find('span', class_ = 'ib published-date').get_text()
                post_time = time_convert(time)
                # get numbers
                j_nums = [num.get_text(strip = True) for num in article.find_all('em', class_ = 'j-count')]
                num1, num2, num3 = (j_nums)
                # update dataframe
                result = result.append(pd.DataFrame({'brandname':[brandname], 'time':[post_time], 'comment_num':[num1], 
                                                     'like_num':[num2], 'share_num':[num3]}),
                                                     ignore_index=True)
                
            except:
                pass
            pass
        pass
    
    result[['comment_num', 'like_num', 'share_num']] = result[['comment_num', 'like_num', 'share_num']].apply(pd.to_numeric)
    result = result.groupby(['brandname', 'time'])[['comment_num', 'like_num', 'share_num']].sum()
    result.reset_index(inplace = True)
    # call function to fill dynamoDB
    fill_table(table, result)
scraper(TABLE, 1)

def lambda_handler(event, context):
    """
    Lambda entrypoint
    """

    extra_logging = {"table": TABLE}
    LOG.info(f"event {event}, context {context}", extra=extra_logging)
    scraper(TABLE, 1)