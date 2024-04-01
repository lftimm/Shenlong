from typing import List, Optional
import urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup

def fetch_data_from_list(fetch_url: str) -> None:
    """
    Writes a file with a link to all manga in MAL.
    :param fetch_url:
    :return:
    """
    if '&show=' not in fetch_url:
        fetch_url += '&show='

    page = 0
    with open('link_list.txt','w',encoding='utf-8') as link_list:
        while True:
            try:
                print(f'current page:{page}')
                html = urlopen(fetch_url+str(page))
                soup = BeautifulSoup(html, 'lxml')

                a_tags = soup.find_all('a')

                url_prefix = 'https://myanimelist.net/manga/'
                for tag in a_tags:
                    href = tag.get('href')
                    if isinstance(href,str) and url_prefix in href:
                        link_list.write(href+'\n')

                page += 50
            except urllib.error.URLError :
                link_list.write('zZ==END OF LIST==Zz')
                break

def fetch_data_from_page(fetch_url: str) -> None:
    ...

def main():
    letters = ['.','A','B','C','D','E','F','G','H','I','J','K',
               'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    url = 'https://myanimelist.net/manga.php?letter='

    for letter in letters:
        print(f'->{letter}')
        fetch_data_from_list(url+letter)

if __name__ == '__main__':
    main()
