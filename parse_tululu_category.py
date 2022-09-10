from urllib.parse import urljoin, urlparse

import requests

from bs4 import BeautifulSoup


URL = 'https://tululu.org/{}'


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    # title, author = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    # img_path = soup.find(class_='bookimage').find('img')['src']
    # comments = soup.select('.texts .black')
    # genres = soup.select('span.d_book a')
    link_book = soup.select_one('div table.d_book a')['href']

    page_book = {
        'link_book': urljoin(URL, link_book)
        # 'title': title,
        # 'author': author,
        # 'image_name': img_path,
        # 'image_url': urljoin(response.url, img_path),
        # 'coments': [comment.text for comment in comments],
        # 'genres': [genre.text for genre in genres]
    }

    return page_book


def main():
    # for book_id in range(1, 10):
    page_book_url_prefix = f'/l55'
    page_book_url = urljoin(URL, page_book_url_prefix)

    session = requests.Session()
    response = session.get(page_book_url)
    response.raise_for_status()

    page_book_content = parse_book_page(response)
    print(page_book_content)

if __name__ == '__main__':
    main()
