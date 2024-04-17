# get a list of programming languages from this page: https://en.wikipedia.org/wiki/List_of_programming_languages
import wikipedia as wp
import requests
import pandas as pd
import bs4 as bs
import time

def find_link(page_links, link_name):
    for term in page_links:
        if term==link_name:
            print(f'Index: {page.links.index(link_name)}\nLink name: {link_name}')

def get_wiki_table(url) -> pd.DataFrame:
    try:
        response = requests.get(url)
    except:
        print('Error accessing Wikipedia table')
    """Take in a response object from extract_sp500_tickers and parse to a dataframe
    :params response: takes in <class 'requests.models.Response'>
    :return: DataFrame of tickers from the Wiki table
    """
    soup = bs.BeautifulSoup(response.text, 'xml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    list_results = []
    for row in table.findAll('tr')[1:]:
        r = row.findAll('td')[0].text
        list_results.append(r)
    df = pd.DataFrame({'ticker': list_results})
    df = df.replace(r'\n','', regex=True) 
    return df

def table_from_html(page_name, table_index):
    html = wp.page(page_name).html()#.encode("UTF-8")
    try: 
        df = pd.read_html(html)[table_index]  # Try 2nd table first as most pages contain contents table first
        # remove last row since it is actually the column headers
        df = df[:-1]
    except IndexError as e:
        print(f'There was an index error: {e}')
        df = pd.read_html(html)[0]
    return df


start = time.time()

page_name = 'timeline of programming language'
first_table_index = 4
last_table_index = 12

frames = []
for table_index in range(first_table_index, last_table_index+1):
    df = table_from_html(page_name, table_index)
    frames.append(df)
df = pd.concat(frames)

df.rename(columns={
    "Year": "year_created"
    ,"Name":"language_name"
    ,"Chief developer, company":"developer"
    ,"Predecessor(s)":"predecessor"
    }, inplace=True)

#df['year_created'] = df['year_created'].replace(['1964?'], '1964')
df['year_created'] = df['year_created'].str.replace('?', '')
df['year_created'] = df['year_created'].str[:4]
df['predecessor'] = df['predecessor'].str.replace('"', '')
df['developer'] = df['developer'].str.replace('"', '')
df['language_name'] = df['language_name'].str.replace("′′",'')

df.to_csv('programming_languages.csv', index=False)

end = time.time()
print(f"Elapsed time: {round((end - start),2)} seconds")