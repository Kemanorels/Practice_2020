import requests
from bs4 import BeautifulSoup


URL = 'https://autosila-amz.com/zapchasti-dlya-sng/vaz/2101/dvigatel/dvigatel/' #Сайт который парсим
# URL = 'https://autosila-amz.com/zapchasti-dlya-inomarok/daewoo/'


def get_html(url, params = None):
    req = requests.get(url, params=params)
    return req

def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    stop = soup.find('span', class_='ty-pagination__selected')
    return stop

get_pages(get_html(URL).text)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ut2-gl__item')
    products = []
    for item in items:
        if item.find('span', class_='ty-price-num') != None:
            products.append({
                'name' : item.find('a', class_='product-title').get_text(),
                'price' : ''.join(item.find('span', class_='ty-price-num').text.split()),
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
    page = 0
    item = []
    while get_pages(get_html(URL, params={'page': page}).text) != None:
        item.append(get_content(get_html(URL, params={'page': page}).text))
        page += 1
        print(f'Парсим страницу{page}')
    print(len(item))


if __name__ == '__main__':
    main()