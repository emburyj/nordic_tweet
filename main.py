# import some packages
import requests
from bs4 import BeautifulSoup as BS
import pathlib
from urllib.request import Request, urlopen
import time

# import environ vars




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

    # for test: load stored html
    def load_inspection_page(name):
        file_path = pathlib.Path(name)
        return file_path.read_text(encoding='utf8')

class Processor():
    def html_proccessor(html):
        '''This function uses BS to process html data to get desired text
        input: html text (string)
        output: list of strings to tweet
        '''
        soup = BS(html)
        # check if Today table has data
        table = Processor.parse_table(soup) # this get html table

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


    def tweet_check():
        '''Use tweepy api to retrieve past tweet data
        input:
        output: list of tweets(str)
        '''
        # global bearer_token, consumer_key, consumer_secret, access_token, access_token_secret

        tweets = client.get_home_timeline()
        past_tweets = []
        for item in tweets[0]:
            past_tweets.append(item)
        return past_tweets

    def groom_tweet_text(groom_name, groom_time):
        # function for generating groom tweet text
        # need to convert UTC to local time
        # include temp
        tweet_text = f"Grooming of {groom_name} has been completed at {groom_time}"
        return tweet_text

    def status_tweet_text(update):
        pass
        # function for generating status report tweet text
class IO():
    def post_tweet(text):
        pass
        # function for posting tweet


# MAIN
if __name__ == '__main__':
# get list of tweets

    while(True):
        # html = get_inspection_page()

        html = load_inspection_page('inspection_page.html')
        soup = BS(html)
        current_table_data = Processor.parse_table(soup)
        # go through list of current data and check if it has been tweeted
        for row in current_table_data:
            current_text = Processor.groom_tweet_text(row[0], row[1])

        time.sleep(60)




    # print(parsed.prettify())