from utils.SearchFilter import SearchFilter
from abc import ABC, abstractmethod
from typing import List

class AnimeWebsite(ABC):
   @abstractmethod
   def apply_filter(self, filters: SearchFilter) -> None:
         raise NotImplementedError('Not implemented')
      
   @abstractmethod 
   def get_url(self, filter: List[str]) -> str:
      raise NotImplementedError('Not implemented')

class SearchStrategy(ABC):
   __website: AnimeWebsite
   
   @abstractmethod
   def execute(self, title: str, filter) -> None:
      pass
   @abstractmethod
   def request_data(self) -> None:
      pass
