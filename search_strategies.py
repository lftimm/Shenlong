from typing import Optional
from project_abcs import SearchStrategy, AnimeWebsite
from utils.Logger import Logger
from utils.SearchFilter import SearchFilter

      
class MyAnimeListWebsite(AnimeWebsite):
   __base_url: str = 'https://myanimelist.net/anime.php?cat=anime'
   __querry_add: str = 'q='   
   __score_filter: str = 'score='
   
   def __init__(self):
      self.score_filter = MyAnimeListWebsite.__score_filter
      
   def apply_filter(self, filter: SearchFilter):
      if filter._score != None:
         self.score_filter += str(filter._score)

   def get_url(self, search: str, filter: Optional[SearchFilter] = None) -> str:
      if filter != None:
         self.apply_filter(filter)
      url: str = '&'.join([MyAnimeListWebsite.__base_url,
                          (MyAnimeListWebsite.__querry_add+search),
                          self.score_filter])
      return url

class MyAnimeListHtmlSearch(SearchStrategy):
   def __init__(self):
      self.__website: AnimeWebsite = MyAnimeListWebsite()
      self.__logger: Logger = Logger.get_instance()
   
   def execute(self, title: str, filter: Optional[SearchFilter] = None) -> None:
      self.__logger.write(f'Started {str(__class__)} execute')
      self.__logger.write(f'Entering get_url method, filter: {filter!=None}')
      url = self.__website.get_url(title, filter)
      self.__logger.write(f'Generated url: {url}')      
      
   def request_data(self):
      pass
   