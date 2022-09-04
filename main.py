import argparse
import os

import requests

from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename


URL = 'https://tululu.org/'


def download_txt(url, filename, folder='books/'):
    response = get_response(url)
    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(url, filename, folder='images/'):
    response = get_response(url)
    folder = sanitize_filepath(folder)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        check_for_redirect(response)
    else:
        return response


def check_for_redirect(response):
    if response.url == URL:
        raise requests.exceptions.HTTPError


def parse_book_page(url):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    img = soup.find(class_='bookimage').find('img')['src']
    img_url = urlsplit(urljoin(URL, img))
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')
    info = {
        'title': title,
        'author': author,
        'image_name': img_url.path,
        'image_url': urljoin(URL, img),
        'coments': [comment.text for comment in comments],
        'genres': [genre.text for genre in genres]
    }
    return info


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
            book_download_url = f'{URL}txt.php?id={book_id}'
            parse_book_url = f'{URL}b{book_id}/'
            names = parse_book_page(parse_book_url)
            download_txt(book_download_url, names['title'], folder='books/')
            download_image(
                names['image_url'], names['image_name'], folder='images/'
                )
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
