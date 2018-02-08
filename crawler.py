from multiprocessing import Pool

import requests
import sys
import csv
from datetime import datetime

from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text  # html-code of pages


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    # Objects of BeautifulSoup
    tds = soup.find('table', id='currencies-all').find_all('td', class_='no-wrap currency-name')

    links = []

    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a  # /currencies/bitcoin/
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = soup.find('h1', class_='text-large').text.strip()  # convert object of the Soup to string
        name = name.replace('\n', '')
        name = name.replace(' ', '')
    except:
        name = ''

    try:
        price = soup.find('span', id="quote_price").text.strip()
    except:
        price = ''

    data = {'name': name, 'price': price}
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(
            (data['name'],
             data['price'])
        )
        print()


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    print('first print = ' + str(sys.argv))
    print('second print = ' + str(sys.argv[1:]))

    start = datetime.now()

    url = 'https://coinmarketcap.com/all/views/all/'

    all_urls = get_all_links(get_html(url))

    # for index, url in enumerate(all_urls):
    #     html = get_html(url)
    #     data = get_page_data(html)
    #     write_csv(data)
    #     print(str(index) + '  ' + data['name'] + ', price = ' + data['price'] + ' parsed.')

    with Pool(30) as p:
        p.map(make_all,
              all_urls)  # передает в передаваемую первым аргументом функцию каждый элемент в списке(второй аргумент)

    end = datetime.now()
    total = end - start
    print('Total time of work the crawler: ' + str(total))


if __name__ == '__main__':
    main()
