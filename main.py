# import some packages
import requests
from bs4 import BeautifulSoup as BS
import pathlib
from urllib.request import Request, urlopen

# import environ vars




# function for scraping html from site
INSPECTION_DOMAIN = 'https://nordic-pulse.com'
INSPECTION_PATH = '/ski-areas/US/OR/Meissner-Sno-Park'
def get_inspection_page():
    url = INSPECTION_DOMAIN+INSPECTION_PATH
    headers={'User-Agent': 'Mozilla/5.0'}
    req = Request(url=url, headers=headers)
    # resp = requests.get(url)
    # resp.raise_for_status()
    # response = resp.text
    page = urlopen(req)
    response = page.read()
    return response

# for test: load stored html
def load_inspection_page(name):
    file_path = pathlib.Path(name)
    return file_path.read_text(encoding='utf8')

# test page
# html = load_inspection_page('inspection_page.html')

# function for parsing html table data
def parse_table(html):
    soup = BS(html)
    tables = soup.find_all('table')
    for table in tables:
        if 'Today' in table.text:
            return table
    return 'nothing to see here'

def parse_rows(html):
    table = parse_table(html)
    rows = table.find_all('tr')
    return rows

# function for parsing html status update data


# function for generating tweet text


# function for posting tweet

# MAIN
if __name__ == '__main__':
    # html = get_inspection_page()

    html = load_inspection_page('inspection_page.html')
    rows = parse_rows(html)
    for row in rows:
        row_items = row.find_all('td')
        if len(row_items) > 0:
            print("Here's the start of a new row:")
            print(row_items[1].text.strip())
            print(row_items[4].text.strip())
            print("ROW END")
            print("***********************************")

        # for item in row_items:
        #     print("Here's an item:")
        #     print(item.text)

    # print(parsed.prettify())