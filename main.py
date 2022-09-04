import requests
import os

from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename

URL = 'https://tululu.org/'


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


def get_url(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        check_for_redirect(response)
    else:
        return response

def check_for_redirect(response):
    if response.url == URL:
        raise requests.exceptions.HTTPError


def get_parse_names(response):
    soup = BeautifulSoup(response.text, 'lxml')
    h1 = soup.find('h1').text.split(' \xa0 :: \xa0 ')
    title, author = h1
    img = soup.find(class_='bookimage').find('img')['src']
    img_url = urlsplit(urljoin(URL, img))
    info = {
        'title': title,
        'image_name': img_url.path,
        'image_url': urljoin(URL, img)
    }
    return info


def main():
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    for book_id in range(1, 11):
        try:
            book_download_url = f'txt.php?id={book_id}'
            parse_book_url = f'b{book_id}/'
            url = f'{URL}{book_download_url}'
            parse_url = f'{URL}{parse_book_url}'
            txt_response = get_url(url)
            parse_response = get_url(parse_url)
            names = get_parse_names(parse_response)
            parse_for_img = get_url(names['image_url'])
            download_txt(txt_response, names['title'], folder='books/')
            download_image(parse_for_img, names['image_name'], folder='images/')
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
