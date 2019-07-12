import csv
import urllib2
from bs4 import BeautifulSoup
from time import sleep

urls = []
output_rows = []


base_page = 'https://business.mentorchamber.org/list'
page = urllib2.urlopen(base_page)
soup = BeautifulSoup(page, 'html.parser')

links1 = soup.find_all('li', attrs={'class': 'mn-subcats-col1'})
links2 = soup.find_all('li', attrs={'class': 'mn-subcats-col2'})


def find_main_links(links):
    for link in links:
        urls.append(link.a.get('href'))
    print('Added all links.')

def parse_listing(listing):
    title = listing.find('div', attrs={'class': 'mn-title'}).text.strip()
    try:
        phone = listing.find('li', attrs={'class': 'mn-phone'}).text.strip()
        row = [title, phone]
    except AttributeError:
        row = [title]
    except TypeError:
        row = [title]
    output_rows.append(row)
    print('Finished listing.')


find_main_links(links1)
find_main_links(links2)


for url in urls:
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find_all('div', attrs={'class': 'mn-listing'})

    for listing in content:
        parse_listing(listing)
        sleep(10)


with open('output.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(output_rows)
