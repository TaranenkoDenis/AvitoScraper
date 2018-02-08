# 1. Выяснить кол-во страниц
# 2. Сформировать кол-во урлов на страницы выдачи
# 3. Собрать данные

import requests
import csv
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-pages')
    all_a_tags = pages.find_all('a', class_='pagination-page')
    last_href = all_a_tags[-1].get('href')

    number_last_page = last_href.split('/')[-1].split('&')[0].split('=')[-1]

    # number_pages = number_last_page

    return int(number_last_page)


def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(
            (
                data['title'],
                data['price'],
                data['metro'],
                data['url']
            )
        )


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads_table_soup = soup.find('div', class_='catalog-list js-catalog-list clearfix')

    ads_soup = ads_table_soup.find_all(
        'div',
        attrs={'class': 'item item_table clearfix js-catalog-item-enum item_without-autoteka ', 'data-type': '1'}
    )

    for ad in ads_soup:
        # title, price, metro, url
        container_for_content = ad.find('div', class_='description item_table-description')

        try:
            title = container_for_content.find('h3').text.strip()
            print(title)
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + container_for_content.find('h3').find('a').get('href')
            print(url)
        except:
            url = ''

        try:
            price = container_for_content.find('div', class_='about').text.strip()
            print(price)
        except:
            price = ''

        try:
            metro = container_for_content.find('div', class_='data').findAll('p')[-1].text
            print(metro)
        except:
            metro = ''

        data = {
            'title': title,
            'price': price,
            'metro': metro,
            'url': url
        }

        write_csv(data)


def main():
    # https://www.avito.ru/moskva/telefony?p=1&q=htc
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = '&q=hts'

    total_pages = get_total_pages(get_html(url='https://www.avito.ru/moskva/telefony?p=1&q=htc'))

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i) + query_part
        print(url_gen)
        page_html = get_html(url_gen)
        get_page_data(page_html)


if __name__ == '__main__':
    main()
