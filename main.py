import requests
import os


URL = 'https://tululu.org/'


def check_for_redirect(response):
    if response.url == URL:
        raise requests.exceptions.HTTPError


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


def main():
    os.makedirs('books', exist_ok=True)
    for i in range(1, 11):
        try:
            download_books(i)
        except requests.exceptions.HTTPError:
            pass

if __name__ == '__main__':
    main()
