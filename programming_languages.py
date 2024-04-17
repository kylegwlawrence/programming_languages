# get a list of programming languages from this page: https://en.wikipedia.org/wiki/List_of_programming_languages
import wikipedia as wp
import requests
import pandas as pd
import bs4 as bs
import time

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

def chronological_programming_langs(save_path):
    """grabs data on programming languages including
    language name, year created, developers (ie the
    creators) and predecessor languages if applicable"""
    
    start = time.time()

    page_name = 'timeline of programming languages'
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
        
    df['year_created'] = df['year_created'].str.replace('?', '')
    df['year_created'] = df['year_created'].str[:4]
    df['predecessor'] = df['predecessor'].str.replace('"', '')
    df['developer'] = df['developer'].str.replace('"', '')
    df['language_name'] = df['language_name'].str.replace("′′",'')

    df.to_csv(save_path, index=False)

    end = time.time()
    print(f"Elapsed time: {round((end - start),2)} seconds")
    
if __name__ == "__main__":
    chronological_programming_langs("programming_languages.csv")