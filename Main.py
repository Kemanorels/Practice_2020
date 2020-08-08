import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://autosila-amz.com/zapchasti-dlya-sng/vaz/2101/dvigatel/dvigatel/' #Сайт который парсим
# URL = 'https://autosila-amz.com/zapchasti-dlya-inomarok/daewoo/'
FILE = 'All_product.csv'

def get_html(url, params = None):
    req = requests.get(url, params=params)
    return req


def get_pages(html):
    '''
    Служит для остановки парсинга, проверяет содержимое страницы'''
    soup = BeautifulSoup(html, 'html.parser')
    stop = soup.find('span', class_='ty-pagination__selected')
    return stop


def save_file(items, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = ';')
            writer.writerow(['name', 'price', 'href'])
            for item in items:
                writer.writerow([item['name'], item['price'], item['href']])


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ut2-gl__item')
    products = []
    for item in items:
        if item.find('span', class_='ty-price-num') != None:
            '''
            проверяет наличие цены (есть позиции без цен)
            добавляет в список
            '''
            products.append({
                'name' : item.find('a', class_='product-title').get_text(),
                'price' : ''.join(item.find('span', class_='ty-price-num').text.split(',')),
                'href' : item.find('a', 'product-title').get('href'),
                })
        else:
            products.append({
                'name' : item.find('a', class_='product-title').get_text(),
                'price' : 'цену уточняйте',
                'href' : item.find('a', 'product-title').get('href'),
                })
    return products


def main():
    page = 1
    items = []
    while get_pages(get_html(URL, params={'page': page}).text) != None:
        '''
        Пока в содержимом страницы есть get_pages, добавляет параметры и парсит страницу
        как только страницы закончатся останавливается
        '''
        items.extend(get_content(get_html(URL, params={'page': page}).text))
        page += 1
        print(f'Парсим страницу {page-1}')
    save_file(items, FILE)


if __name__ == '__main__':
    main()