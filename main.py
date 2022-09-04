import requests
import os

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


def get_parse_names(url):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    img = soup.find(class_='bookimage').find('img')['src']
    img_url = urlsplit(urljoin(URL, img))
    comments = soup.select('.texts .black')
    info = {
        'title': title,
        'image_name': img_url.path,
        'image_url': urljoin(URL, img),
        'coments': comments
    }
    return info


def main():
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    for book_id in range(1, 11):
        try:
            book_download_url = f'{URL}txt.php?id={book_id}'
            parse_book_url = f'{URL}b{book_id}/'
            names = get_parse_names(parse_book_url)
            download_txt(book_download_url, names['title'], folder='books/')
            download_image(names['image_url'], names['image_name'], folder='images/')
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
