from utils.project_abcs import SearchStrategy, AnimeWebsite
from utils.Logger import Logger
from utils.AnimeUtils import SearchFilter, AnimeData 

from typing import List, Optional
from requests import Response
from bs4 import BeautifulSoup

import requests

class MyAnimeListWebsite(AnimeWebsite):
   __base_url: str = 'https://myanimelist.net/anime.php?cat=anime'
   __querry_add: str = 'q='   
   __score_filter: str = 'score='
   __type_filter: str = 'type='
   
   def __init__(self):
      self.__logger = Logger.get_instance()
      self.score_filter = MyAnimeListWebsite.__score_filter
      self.type_filter = MyAnimeListWebsite.__type_filter
      
   def apply_filter(self, filter: SearchFilter):
      if filter._score != None:
         self.score_filter += str(filter._score)
         
      if(filter._type.lower() == 'tv'):
         self.type_filter += str(1)
      elif filter._type.lower() == 'ova':
         self.type_filter += str(2)
      elif filter._type.lower() == 'movie':
         self.type_filter += str(3)
      elif filter._type.lower() == 'special':
         self.type_filter += str(4)
      elif filter._type.lower() == 'ona':
         self.type_filter += str(5) 
      else:
         self.type_filter += str(0)

   def get_url(self, search: str, filter: Optional[SearchFilter] = None) -> str:
      if filter != None:
         self.apply_filter(filter)
      url: str = '&'.join([MyAnimeListWebsite.__base_url,
                          (MyAnimeListWebsite.__querry_add+search),
                          self.score_filter,
                          self.type_filter])
      return url
   
   def get_from_search_list(self, search_page: Response) -> Response:
      self.__logger.write(f'Entering get_from_search_list() with : {search_page.url}')
      soup = BeautifulSoup(search_page.content, 'html.parser')
      result = soup.find('div',{'class':'title'}).a['href']
      self.__logger.write(f'Returning with : {result}')
      return result
   
   def get_anime_info(self, anime_page: Response) -> AnimeData:
      soup: BeautifulSoup = BeautifulSoup(anime_page.content, 'html.parser')
      
      title = soup.find('h1', {'class':'title-name h1_bold_none'}).text
      image = soup.find('img', {'alt':title})['data-src']
      score = soup.find('span', {'itemprop':'ratingValue'}).text
      ttype = soup.find('span', {'class':'information type'}).find('a').text
      status = soup.find('span', string='Status:').next.next
      studio = soup.find('span', {'class':'information studio author'}).find('a').text
      genres : List[str] = [tag.text for tag in soup.findAll('span', {'itemprop':'genre'})[:-1]]
      demographics = soup.findAll('span', {'itemprop':'genre'})[-1].text

      result = AnimeData(_cover_image = image,
                         _title = title,
                         _score = score,
                         _type = ttype,
                         _status = status.strip(),
                         _studio = studio,
                         _genres = genres,
                         _demographics = demographics)
      
      self.__logger.write(f'Result: {result}')

      return result

class MyAnimeListHtmlSearch(SearchStrategy):
   __search_page: Response
   __anime_page: Response
   result: AnimeData
     
   def __init__(self, mal_website: MyAnimeListWebsite):
      self.__website: MyAnimeListWebsite = mal_website()
      self.__logger: Logger = Logger.get_instance()
   
   def execute(self, title: str, filter: Optional[SearchFilter] = None) -> None:
      self.__logger.write(f'Started {str(__class__)} execute')
      self.__logger.write(f'Entering get_url method, filter: {filter!=None}')
      
      url: str = self.__website.get_url(title, filter)
      
      self.__logger.write(f'Generated url: {url}')
         
      MyAnimeListHtmlSearch.__search_page = self.request_data(url)
      
   def request_data(self, url: str) -> Response:
      if url is None:
         self.__logger.write(f'No page url was received')
         raise ValueError(f'request_data() needs a url not none')   

      try:
         website: Response = requests.get(url)
         website.raise_for_status()  # Raises an HTTPError for bad responses
      except requests.exceptions.RequestException as e:
         self.__logger.write(f'HTTP Request failure: {e}')

      self.__logger.write(f'Request Successful') 
      return website
   
   def get_result_page(self) -> None:
      self.__logger.write(f'Started {str(__class__.__name__)} get_result_page()')
      page_url = self.__website.get_from_search_list(MyAnimeListHtmlSearch.__search_page)
      MyAnimeListHtmlSearch.__anime_page = self.request_data(page_url)
      MyAnimeListHtmlSearch.result = self.__website.get_anime_info(MyAnimeListHtmlSearch.__anime_page) 
   
   def get_result(self) -> AnimeData:
      return str(MyAnimeListHtmlSearch.result)