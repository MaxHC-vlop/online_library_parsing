import argparse
import os
import logging
import time

import requests

from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename


URL = 'https://tululu.org/{}'


def download_txt(url,  book_id, filename, folder='books/'):
    book_payload = {'id': book_id}
    session = requests.Session()
    response = session.get(url, params=book_payload)
    response.raise_for_status()
    check_for_redirect(response)

    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(url, filename, folder='images/', payload=None):
    session = requests.Session()
    response = session.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)

    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    img_path = soup.find(class_='bookimage').find('img')['src']
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')
    book_url = soup.select('table.d_block a[href*="/txt"]')
    print(book_url)

    page_book = {
        'title': title,
        'author': author,
        'image_name': img_path,
        'book_url': urljoin(response.url, book_url),
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

    sleep_time = 1
    try:
        for books_pages in range(args.start_page, args.end_page):

            page_book_url_prefix = f'/l55/{books_pages}'
            page_book_url = urljoin(URL, page_book_url_prefix)

            session = requests.Session()
            response = session.get(page_book_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')
            link_page = soup.select('.bookimage a[href]')
            links = [urljoin(URL, link['href']) for link in link_page]

            for book_page in links:
                print(book_page)
                # page_book_url_prefix = f'b{book_id}/'

                session = requests.Session()
                response = session.get(book_page)
                response.raise_for_status()
                check_for_redirect(response)
                page_book_content = parse_book_page(response)
                print(page_book_content)

                # download_txt(
                #     book_url, book_id, page_book_content['title'], folder='books/'
                #     )
                download_image(
                    page_book_content['image_url'], page_book_content['image_name'],
                    folder='images/'
                    )

    except requests.exceptions.HTTPError as errh:
        logging.error(errh, exc_info=True)
    except requests.exceptions.ConnectionError as errc:
        logging.error(errc, exc_info=True)
        time.sleep(sleep_time)
        sleep_time += 1

if __name__ == '__main__':
    main()
