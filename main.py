import argparse
import os
import logging

import requests

from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename


URL = 'https://tululu.org/{}'


def download_txt(response, filename, folder='books/'):
    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(response, filename, folder='images/'):
    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_response(url, payload=None):
    session = requests.Session()
    response = session.get(url, params=payload)
    if response.history:
        check_for_redirect()

    return response


def check_for_redirect():
    raise requests.exceptions.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    img_path = soup.find(class_='bookimage').find('img')['src']
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')

    page_book = {
        'title': title,
        'author': author,
        'image_name': img_path,
        'image_url': urljoin(response.url, img_path),
        'coments': [comment.text for comment in comments],
        'genres': [genre.text for genre in genres]
    }

    return page_book


def main():
    parser = argparse.ArgumentParser(
        description='Download book and image from tululu.org'
        )
    parser.add_argument(
        'start_page', help='--start_page', nargs='?', type=int, default=1
        )
    parser.add_argument(
        'end_page', help='--end_page', nargs='?', type=int, default=2
        )
    args = parser.parse_args()
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    for book_id in range(args.start_page, args.end_page):
        try:
            book_url_prefix = 'txt.php'
            payload_book = {'id': book_id}
            book_url = urljoin(URL, book_url_prefix)
            book_response = get_response(book_url, payload_book)

            page_book_url_prefix = f'b{book_id}/'
            page_book_url = urljoin(URL, page_book_url_prefix)
            responce_for_parse = get_response(page_book_url)
            page_book_responce = parse_book_page(responce_for_parse)

            image_responce = get_response(page_book_responce['image_url'])

            download_txt(
                book_response, page_book_responce['title'], folder='books/'
                )
            download_image(
                image_responce, page_book_responce['image_name'],
                folder='images/'
                )

        except Exception as err:
            logging.error(err, exc_info=True)

if __name__ == '__main__':
    main()
