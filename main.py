from bs4 import BeautifulSoup
import requests
from pprint import pprint

html_text = requests.get('https://www.craigslist.org/about/sites').text
soup = BeautifulSoup(html_text, 'lxml')
us_data = soup.find('div', class_='colmask')
cities = us_data.find_all('a', href=True)
cities_list = []
for city in cities:
    cities_list.append((city.text,city['href']))

print(f"Total cities: (len{cities_list})")

city_count = 0
post_count = 0

for city in cities_list:
    city_name = city[0]
    city_url = city[1]
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


