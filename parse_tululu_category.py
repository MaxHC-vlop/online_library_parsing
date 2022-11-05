import argparse
import os
import logging
import time
import json

import requests

from pathvalidate import sanitize_filepath, sanitize_filename
from urllib.parse import urljoin
from bs4 import BeautifulSoup


URL = 'https://tululu.org/{}'


def download_txt(url, filename, folder='books/'):
    session = requests.Session()
    response = session.get(url)
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
    parser.add_argument('--start_page', default=1, type=int,
        help='First download page')

    parser.add_argument('--end_page', default=702, type=int,
        help='Last download page')

    parser.add_argument('--dest_folder', default='content',
        help='Directory for storing uploaded files')

    parser.add_argument('--skip_imgs', action='store_true',
        help='Do not download pictures')

    parser.add_argument('--skip_txt', action='store_true',
        help='Do not download books')

    parser.add_argument('--json_path', default='.',
        help='Json file storage directory')

    args = parser.parse_args()

    return args


def main():

    args = get_user_args()

    books_folder = os.path.join(
        args.dest_folder,
        'books'
        )
    os.makedirs(books_folder, exist_ok=True)

    image_folder = os.path.join(
        args.dest_folder,
        'images'
        )
    os.makedirs(image_folder, exist_ok=True)

    json_folder = os.path.join(
        args.json_path
        )
    os.makedirs(json_folder, exist_ok=True)

    filename = f'{args.json_path}{os.sep}books_content.json'

    sleep_time = 1

    books = []

    for number_2, books_pages in enumerate(range(args.start_page, args.end_page)):
        try:
            page_book_url_prefix = f'/l55/{books_pages}'
            page_book_url = urljoin(URL, page_book_url_prefix)

            session = requests.Session()
            response = session.get(page_book_url)
            response.raise_for_status()
            check_for_redirect(response)

            soup = BeautifulSoup(response.text, 'lxml')
            parsed_links = soup.select('.bookimage a[href]')
            links = [urljoin(page_book_url, link['href']) for link in parsed_links]

        except requests.exceptions.HTTPError as errh:
            logging.error(errh, exc_info=True)

        except requests.exceptions.ConnectionError as errc:
            logging.error(errc, exc_info=True)
            time.sleep(sleep_time)
            sleep_time += 1

        for number, book_page in enumerate(links):
            try:
                session = requests.Session()
                response = session.get(book_page)
                response.raise_for_status()
                check_for_redirect(response)

                page_book_content = parse_book_page(response)


                image1 = page_book_content['image_name'].replace('/', '')

                image = f'..{os.sep}content{os.sep}images{os.sep}{image1}'

                book_path = f'book_{number_2}.{number}'

                filepath = f'..{os.sep}content{os.sep}books{os.sep}{book_path}.txt'

                book_content = {
                    'title': page_book_content['title'],
                    'author': page_book_content['author'],
                    'img_src': image,
                    'book_path': filepath,
                    'comments': page_book_content['coments'],
                    'genres': page_book_content['genres'],
                }

                books.append(book_content)

                if not args.skip_txt:
                    download_txt(
                        page_book_content['book_url'],
                        book_path,
                        books_folder
                        )

                if not args.skip_imgs:
                    download_image(
                        page_book_content['image_url'],
                        page_book_content['image_name'],
                        folder=image_folder
                        )

            except TypeError as errt:
                print('None in download link: {0}'.format(errt))
                continue

            except requests.exceptions.HTTPError as errh:
                logging.error(errh, exc_info=True)

            except requests.exceptions.ConnectionError as errc:
                logging.error(errc, exc_info=True)
                time.sleep(sleep_time)
                sleep_time += 1

        with open(filename, "w", encoding='utf-8') as file:
            json.dump(books, file, indent=7, ensure_ascii=False)


if __name__ == '__main__':
    main()
