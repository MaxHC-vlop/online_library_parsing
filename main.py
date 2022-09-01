import requests
import os


def check_for_redirect(responce):
    try:
        pass
    except requests.HTTPError:
        raise


def main():
    os.makedirs('books', exist_ok=True)
    for i in range(1, 11):
        url = f"https://tululu.org/txt.php?id={i}"
        response = requests.get(url)
        if response.history:
            check_for_redirect(response)
            pass
        response.raise_for_status() 
        filepath = f'books/kniga{i}.txt'
        with open(filepath, 'wb') as file:
            file.write(response.content)

if __name__ == '__main__':
    main()