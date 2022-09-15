import argparse
import os
import logging
import time
import json

from download_file import download_image, download_txt
from download_file import check_for_redirect

import requests

from urllib.parse import urljoin
from bs4 import BeautifulSoup


URL = 'https://tululu.org/{}'


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.select_one('h1').text.split(' \xa0 :: \xa0 ')
    img_path = soup.select_one('table.d_book div.bookimage img')['src']
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')
    book_url = soup.select_one('table.d_book tr td a[href*="/txt.php?id="]')

    page_book = {
        'title': title,
        'author': author,
        'image_name': img_path,
        'book_url': urljoin(response.url, book_url['href']),
        'image_url': urljoin(response.url, img_path),
        'coments': [comment.text for comment in comments],
        'genres': [genre.text for genre in genres]
    }

    return page_book


def get_user_args():
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

    return args


def main():
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    filename = 'books_content.json'

    sleep_time = 1

    books = []
    for books_pages in range(4, 5): # args.start_page, args.end_page
        try:
            page_book_url_prefix = f'/l55/{books_pages}'
            page_book_url = urljoin(URL, page_book_url_prefix)

            session = requests.Session()
            response = session.get(page_book_url)
            response.raise_for_status()
            check_for_redirect(response)

            soup = BeautifulSoup(response.text, 'lxml')
            link_page = soup.select('.bookimage a[href]')
            links = [urljoin(URL, link['href']) for link in link_page]

        except requests.exceptions.HTTPError as errh:
            logging.error(errh, exc_info=True)
    
        except requests.exceptions.ConnectionError as errc:
            logging.error(errc, exc_info=True)
            time.sleep(sleep_time)
            sleep_time += 1

        for book_page in links:
            try:
                session = requests.Session()
                response = session.get(book_page)
                response.raise_for_status()
                check_for_redirect(response)

                page_book_content = parse_book_page(response)

                book_path = page_book_content['title']

                book_content = {
                    'title': page_book_content['title'],
                    'author': page_book_content['author'],
                    'img_src': page_book_content['image_name'],
                    'book_path': f'books/{book_path}.txt',
                    'comments': page_book_content['coments'],
                    'genres': page_book_content['genres'],
                }

                books.append(book_content)

                download_txt(
                    page_book_content['book_url'], page_book_content['title'], folder='books/'
                    )
                download_image(
                    page_book_content['image_url'], page_book_content['image_name'],
                    folder='images/'
                    )

            except TypeError as errt:
                print('None in download link: {0}'.format(errt))
                continue


        with open(filename, "w", encoding='utf-8') as my_file:
            json.dump(books, my_file, indent=7 ,ensure_ascii=False)


if __name__ == '__main__':
    main()
