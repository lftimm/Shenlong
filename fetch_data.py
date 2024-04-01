import urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os


def fetch_data_from_list(fetch_url: str, letter: str) -> None:
    """
    Writes a file with a link to all manga in MAL.
    :param letter:
    :param fetch_url:
    :return:
    """
    if '&show=' not in fetch_url:
        fetch_url += '&show='

    page = 0
    with open(f'link_list_{letter}_.txt', 'w', encoding='utf-8') as link_list:
        while True:
            try:
                print(f'current page:{page}')
                html = urlopen(fetch_url + str(page))
                soup = BeautifulSoup(html, 'lxml')

                a_tags = soup.find_all('a')

                url_prefix = 'https://myanimelist.net/manga/'
                for tag in a_tags:
                    href = tag.get('href')
                    if isinstance(href, str) and url_prefix in href:
                        link_list.write(href + '\n')

                page += 50
            except urllib.error.URLError:
                link_list.write('zZ==END OF LIST==Zz')
                break

def join_fetched_data() -> None:
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    manga_links = []

    with open('final_list.txt', 'w', encoding='utf-8') as final_list:
        for letter in letters:
            with open(f'link_list_{letter}_.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                unique = list(dict.fromkeys(lines))

                for link in unique:
                    final_list.write(link+'\n')


    '''
    with open('final_list.txt', 'w') as f:
        for link in final:
            f.write(link+'\n')
    '''

def fetch_data_from_page(fetch_url: str) -> None:
    ...

def main():
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    url = 'https://myanimelist.net/manga.php?letter='

    if 'final_list.txt' not in os.listdir():
        for letter in letters:
            print(f'->{letter}')
            fetch_data_from_list(url + letter, letter)

        join_fetched_data()

    else:
        print('List of links present')
        exit(0)


if __name__ == '__main__':
    main()
