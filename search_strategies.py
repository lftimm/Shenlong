from project_abcs import SearchStrategy, AnimeWebsite
from utils.Logger import Logger
from utils.AnimeUtils import SearchFilter, AnimeData 

from typing import Optional
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
         else: self.type_filter += str(0)


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
      self.__logger.write(f'Entering get_anime_info()')
      soup = BeautifulSoup(anime_page.content, 'html.parser')

      two_n_siblings = lambda x: x.next_sibling.next_sibling
      four_n_siblings = lambda x: two_n_siblings(two_n_siblings(x))
      eight_n_siblings = lambda x: four_n_siblings(four_n_siblings(x))

      title = soup.find('h1', {'class':'title-name h1_bold_none'}).text    
      image = soup.find('img',{'alt':f'{title}'})['data-src']
      
      all_h2s = soup.findAll('h2')
      information_tag = all_h2s[1].next_sibling if all_h2s != None else None
      
      type_tag = information_tag.next_sibling
      ttype = type_tag.a['href'] if type_tag != None else None
      self.__logger.write(f'type: {ttype}')

      status_tag = four_n_siblings(type_tag)
      status = status_tag.span.next_sibling.text
      self.__logger.write(f'status: {status}')

      
      studio_tag = four_n_siblings(eight_n_siblings(status_tag))
      studio = studio_tag.find('a').text if studio_tag != None else None
      self.__logger.write(f'studio: {studio}')

      genres_tag = four_n_siblings(studio_tag)
      genres = [tag.text if tag != None else None for tag in genres_tag.findAll('span',{'itemprop':'genre'})]
      self.__logger.write(f'genres: {genres}')

      demographics_tag = two_n_siblings(genres_tag)
      demographics = demographics_tag.a.text if demographics_tag != None else None

      statistics_tag = all_h2s[2]
      score_tag = two_n_siblings(statistics_tag)
      score = score_tag.find('span',{'itemprop':'ratingValue'}).text if score_tag != None else None

      result = AnimeData(_cover_image=image,
                       _title=title,
                       _score=score,
                       _type=ttype,
                       _status=status,
                       _studio=studio,
                       _demographics=demographics,
                       _genres=genres)
      
      self.__logger.write(result)

      return result

class MyAnimeListHtmlSearch(SearchStrategy):
   __search_page: Response
   __anime_page: Response
   __result: AnimeData
     
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
         
      self.__logger.write(f'Requesting data for {url}')
      website: Response = requests.get(url)
      if (not website.ok):
         self.__logger.write(f'HTTP Request failure {website.status_code}')      
      else: 
         self.__logger.write(f'Request Sucessful') 
      
      return website
   
   def get_result_page(self) -> None:
      self.__logger.write(f'Started {str(__class__.__name__)} get_result_page()')
      page_url = self.__website.get_from_search_list(MyAnimeListHtmlSearch.__search_page)
      MyAnimeListHtmlSearch.__anime_page = self.request_data(page_url)
      MyAnimeListHtmlSearch.__result = self.__website.get_anime_info(MyAnimeListHtmlSearch.__anime_page)

   def get_result(self) -> AnimeData:
      return MyAnimeListHtmlSearch.__result