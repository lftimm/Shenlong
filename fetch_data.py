from typing import Dict, List
import os
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
import time


def fetch_data_from_list(fetch_url: str, letter: str) -> None:
    if '&show=' not in fetch_url:
        fetch_url += '&show='

    page = 0
    with open(f'link_list_{letter}_.txt', 'w', encoding='utf-8') as link_list:
        while True:
            try:
                print(f'current page:{page}')
                html = requests.get(fetch_url + str(page))
                soup = BeautifulSoup(html, 'lxml')

                a_tags = soup.find_all('a')

                url_prefix = 'https://myanimelist.net/manga/'
                for tag in a_tags:
                    href = tag.get('href')
                    if isinstance(href, str) and url_prefix in href:
                        link_list.write(href + '\n')

                page += 50
            except requests.exceptions.RequestException:
                link_list.write('zZ==END OF LIST==Zz')
                break


def join_fetched_data() -> None:
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    with open('final_list.txt', 'w', encoding='utf-8') as final_list:
        for letter in letters:
            with open(f'link_list_{letter}_.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                unique = list(dict.fromkeys(lines))

                for link in unique:
                    final_list.write(link + '\n')


def write_to_csv(data: List[Dict]) -> None:
    with open('manga_data.csv', 'w', newline='', encoding='utf-8') as csvf:
        fields = ['Title', 'Volumes', 'Chapters', 'Status',
                  'Published', 'Genres', 'Score']
        writer = csv.DictWriter(csvf, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


async def fetch_and_parse_the_page(lines:List[str]) -> List[BeautifulSoup]:
    soups = []
    async with aiohttp.ClientSession() as session:
        for i, link in enumerate(lines):
            start_time = time.time()  # Start timing
            async with session.get(link) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                soups.append(soup)
            end_time = time.time()  # End timing
            print(f'Request {i+1}/{len(lines)} time for {link}: {end_time - start_time} seconds')  # Print request time
    return soups


def fetch_data_from_page(b_soup=None) -> Dict:
    soup = b_soup
    entry = {}
    a_tags = soup.find_all('a')
    div_tags = soup.find_all('div', {'class': 'spaceit_pad'})

    title = soup.find('span', {'class': 'h1-title'}).text
    entry['Title'] = title

    for tag in div_tags:
        span = tag.find_next('span', class_='dark_text')
        if span:
            key = span.text.strip().rstrip(':')
            value = span.next_sibling.strip()

            if key in ['Volumes', 'Chapters', 'Status', 'Published']:
                entry[key] = value

    genres = []
    for tag in a_tags:
        href = str(tag.get('href'))
        if '/manga/genre/' in href:
            genres.append(href.split('/')[-1])

    entry['Genres'] = genres

    score = soup.find('span', {'itemprop': 'ratingValue'})
    if score:
        text_score = score.text.replace(',', '.')
        entry['Score'] = text_score
    else:
        entry['Score'] = None

    return entry


def main():
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    url = 'https://myanimelist.net/manga.php?letter='

    if 'final_list.txt' not in os.listdir():
        for letter in letters:
            print(f'->{letter}')
            fetch_data_from_list(url + letter, letter)

        join_fetched_data()

    with open('final_list.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        data = []
        soups = asyncio.run(fetch_and_parse_the_page(lines))
        for soup in soups:
            data.append(fetch_data_from_page(soup))
        write_to_csv(data)


if __name__ == '__main__':
    main()
