# Load libraries
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint

# File paths
city_update = 'city_update.txt'
city_file = 'cl-cities.csv'

# Get list of CL cities and their URLs
html_text = requests.get('https://www.craigslist.org/about/sites').text
soup = BeautifulSoup(html_text, 'lxml')
# print("In the soup")
us_data = soup.find('div', class_='colmask')
# print("parsing US data")
cities = us_data.find_all('a', href=True)
cities_list = []
for city in cities:
    cities_list.append((city.text,city['href']))
    # print(city.text, city['href'])

cities_df = pd.DataFrame(cities_list, columns = ['name', 'url'])

print(f"Total cities: {len(cities_list)}")

# pprint(cities_df)

cities_df.to_csv(city_file, index=False, encoding='utf-8')

date_txt = datetime.today().strftime('%Y-%m-%d')
print(date_txt)
text_file = open(city_update, 'w')
n = text_file.write(date_txt)
print(n)
text_file.close()
