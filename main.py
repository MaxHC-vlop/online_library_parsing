import requests
import os

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename

URL = 'https://tululu.org/'


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        check_for_redirect(response)
    else:
        folder = sanitize_filepath(folder)
        filename = sanitize_filename(filename)
        filepath = os.path.join(folder, f'{filename}.txt')
        with open(filepath, 'wb') as file:
            file.write(response.content)


def check_for_redirect(response):
    if response.url == URL:
        raise requests.exceptions.HTTPError


def get_parse_names(id):
    url = f'{URL}{id}'
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        check_for_redirect(response)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = soup.find('h1').text.split(' \xa0 :: \xa0 ')
        title, author = h1
        return title


def main():
    os.makedirs('books', exist_ok=True)
    for book_id in range(1, 11):
        try:
            book_download_url = f'txt.php?id={book_id}'
            parse_book_url = f'b{book_id}/'
            url = f'{URL}{book_download_url}'
            download_txt(url, get_parse_names(parse_book_url), folder='books/')
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
