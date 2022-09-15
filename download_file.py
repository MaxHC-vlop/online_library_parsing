import os

import requests

from pathvalidate import sanitize_filepath, sanitize_filename


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