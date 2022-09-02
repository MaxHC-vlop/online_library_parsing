import requests
import os

from bs4 import BeautifulSoup


URL = 'https://tululu.org/'


def download_books(i):
    book_url = f"{URL}txt.php?id={i}"
    response = requests.get(book_url)
    if response.history:
        check_for_redirect(response)
    else:
        response.raise_for_status()
        filepath = f'books/kniga{i}.txt'
        with open(filepath, 'wb') as file:
            file.write(response.content)



def check_for_redirect(response):
    if response.url == URL:
        raise requests.exceptions.HTTPError


def get_parse_names():
    url = 'https://tululu.org/b1/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    h1 = soup.find('h1')
    qwe = h1.text
    qw = qwe.split(' \xa0 :: \xa0 ')
    title, author = qw
    print(f'Заголовок: {title}\nАвтор: {author}')


def main():
    os.makedirs('books', exist_ok=True)
    for i in range(1, 11):
        try:
            download_books(i)
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
