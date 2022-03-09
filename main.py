# Load libraries
import sys
import time
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from pprint import pprint

# Define Functions

# Get / Update Cities
def city_info(days):
    # Has it been more than a week?
    if days > 7:
        # Get list of CL cities and their URLs
        print("city_info: Updating city list")
        html_text = requests.get('https://www.craigslist.org/about/sites').text
        soup = BeautifulSoup(html_text, 'lxml')
        us_data = soup.find('div', class_='colmask')
        cities = us_data.find_all('a', href=True)
        cities_list = []
        for city in cities:
            cities_list.append((city.text,city['href']))

        cities_df = pd.DataFrame(cities_list, columns = ['name', 'url'])
        cities_df.to_csv(city_file, index=False, encoding='utf-8')

        date_txt = datetime.today().strftime('%Y-%m-%d')
        text_file = open(city_update, 'w')
        n = text_file.write(date_txt)
        text_file.close()

    else:
        print("city_info: Reading city list")
        cities_df = pd.read_csv(city_file)

    print(f"city_info: Total cities: {len(cities_list)}")

    return cities_df

# File paths
city_update = 'city_update.txt'
city_file = 'cl-cities.csv'

# Get date of last city list update
text_file = open(city_update, 'r')
last_update_str = text_file.read()
text_file.close()

date_format = '%Y-%m-%d'
curr_date = datetime.today().strftime(date_format)
current_date = datetime.strptime(curr_date, date_format)
last_update = datetime.strptime(last_update_str, date_format)
delta = current_date - last_update

print(f"main: Cities list last updated {delta.days} days ago")

citylist_df = city_info(delta.days)

sys.exit()

# Step through cities list
city_count = 0
post_count = 0

for index, row in citylist_df.iterrows():
    city_name = row['name']
    city_url = row['url']
    city_count += 1
    #print(f"City #{city_count}: {city_name }")

    html_text = requests.get(city_url+'search/boo?query=macgregor+%2826m%7C26x%29&purveyor-input=all&srchType=T').text
    soup = BeautifulSoup(html_text, 'lxml')
    results = soup.find_all('li', class_='result-row')
    print(f"Number of results: {len(results)}")
    print()

    for result in results:
        result_link = result.find('a', class_='result-title hdrlnk')
        pid = result_link['data-id']
        title = result_link.text
        link = result_link['href']
        img_link = result.find('img')
        price = result.span.text
        date_time = result.time['datetime']
        post_count += 1

        #print(result)
        print()

        print(f"Posting #: {post_count}")
        print(f"PID: {pid}")
        print(f"Date / Time: {date_time}")
        print(f"Title: {title}")
        print(f"Image Link: {img_link}")
        print(f"Price: {price}")
        print(f"City: {city_name}")
        print(f"Link: {link}")
        print()

print()
print(f"Total posting results: {post_count}")


