import requests

from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
post = soup.find(class_='entry-content')
h1 = soup.find(class_='entry-title')
image = soup.find(class_='attachment-post-image')['src']
print(h1.text, image, post.text,sep='\n')