import requests
from bs4 import BeautifulSoup


URL = 'https://autosila-amz.com/zapchasti-dlya-sng/vaz/2101/dvigatel/dvigatel/' #Сайт который парсим
# URL = 'https://autosila-amz.com/zapchasti-dlya-inomarok/daewoo/'


def get_html(url, params = None):
    req = requests.get(url, params=params)
    return req

def get_pages(html):
    pass


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
    for prod in products:
        print(prod)
    return products



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('error')


parse()



# if __name__ == '__main__':
# 	main()