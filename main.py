#!/usr/bin/python3
# import some packages

from bs4 import BeautifulSoup as BS
import pathlib
from urllib.request import Request, urlopen
import time
import os
import tweepy

# import environ vars
bearer_token = os.environ["BEARER_TOKEN"]
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
client = tweepy.Client(bearer_token=bearer_token,
               consumer_key=consumer_key,
               consumer_secret=consumer_secret,
               access_token=access_token,
               access_token_secret=access_token_secret)


# function for scraping html from site
INSPECTION_DOMAIN = 'https://nordic-pulse.com'
INSPECTION_PATH = '/ski-areas/US/OR/Meissner-Sno-Park'
class Data():
    def get_inspection_page():
        url = INSPECTION_DOMAIN+INSPECTION_PATH
        headers={'User-Agent': 'Mozilla/5.0'}
        req = Request(url=url, headers=headers)
        page = urlopen(req)
        response = page.read()
        return response

    # for test: load locally stored html
    def load_inspection_page(name):
        file_path = pathlib.Path(name)
        return file_path.read_text(encoding='utf8')

    def tweet_check():
        '''Use tweepy api to retrieve past tweet data
        input:
        output: list of tweets(str)
        '''
        global client

        tweets = client.get_home_timeline()
        past_tweets = []
        if tweets[0]:
            for item in tweets[0]:
                past_tweets.append(str(item))
        return past_tweets

class Processor():
    # function for parsing html table data
    def parse_table(soup):
        '''This function parses a BS object to get grooming data from Today table
        input: BeautifulSoup object
        output: List of [route(str), datetime(str)]
        '''
        table_data = []
        tables = soup.find_all('table')
        for table in tables:
            if 'Today' in table.text:
                table_html = table
        rows = table_html.find_all('tr')
        for row in rows:
            row_items = row.find_all('td')
            if len(row_items) > 0:
                table_data.append([row_items[1].text.strip(), row_items[4].text.strip()])
        return table_data

    def parse_status(soup):
        html = soup.find_all('npl-reports-single')
        status_data = html[0].find_all('p')
        status_text = status_data[0].text.strip()
        poster_data = html[0].find_all('span')
        poster = poster_data[-1].text.strip()
        status_text = f"{status_text}\nPosted by {poster}"
        return status_text

    def parse_temp(soup):
        html = soup.find_all('npl-weather')
        temp_html = html[0].find_all('span')
        temp_data = temp_html[1].text.split()
        temp_tweet = f"\nCurrent temperature is {temp_data[0]}."
        return temp_tweet

    def groom_tweet_text(groom_name, groom_time):
        # function for generating groom tweet text
        # need to convert UTC to local time
        # include temp
        groom_dt = groom_time.split(',')
        tweet_text = f"{groom_name} has been groomed. Completed at {groom_dt[1].strip()} on {groom_dt[0].strip()}."
        return tweet_text

    def convert_tz(groom_time):
        datetime_list = groom_time.split(', ') # split date from time
        time_list = datetime_list[1].split(' ') # list of [hr:min, AM/PM]
        time_str = time_list[0].split(':') # list of [hr, min]
        hr = int(time_str[0])
        if hr > 8:
            hr = hr - 8
        else:
            if hr < 8:
                if time_list[-1] == "PM":
                    time_list[-1] = "AM"
                else:
                    time_list[-1] = "PM"
            hr = hr - 8 + 12

        time_str[0] = str(hr)
        time_list[0] = ":".join(time_str)
        datetime_list[1] = " ".join(time_list)
        return ", ".join(datetime_list)

class IO():
    def post_tweet(text):
        '''This function will use tweepy api to post a new tweet
        input: text (str)
        output: void
        '''
        global client
        client.create_tweet(text=text)

# MAIN
if __name__ == '__main__':
# get list of past tweets
    past_tweets = Data.tweet_check()

    html = Data.get_inspection_page()
    new_tweet_text = []
    # html = Data.load_inspection_page('inspection_page.html')
    soup = BS(html, features="html5lib")
    current_table_data = Processor.parse_table(soup)
    temp_tweet = Processor.parse_temp(soup)
    current_status = Processor.parse_status(soup)
    # go through list of current data and check if it has been tweeted
    for current in current_table_data:
        current_text = Processor.groom_tweet_text(current[0], current[1])
        # current_text = Processor.groom_tweet_text(current[0], Processor.convert_tz(current[1]))
        flag = True
        for past in past_tweets:
            # check if current line in table corresponds to a previous tweet
            if current_text in past:
                flag = False
        if flag:
            new_tweet_text.append(current_text + temp_tweet) # this indicates it hasn't been tweeted
    flag = True
    for past in past_tweets:
        if current_status in past:
            flag = False
    if flag:
        new_tweet_text.append(current_status + temp_tweet)
    for text in new_tweet_text:
        IO.post_tweet(text)
        print(text)
        past_tweets.append(text)
