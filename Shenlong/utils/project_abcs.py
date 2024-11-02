from .AnimeUtils import SearchFilter

from abc import ABC, abstractmethod
from typing import Optional

class AnimeWebsite(ABC):
   __base_url : str 
   
   @abstractmethod
   def apply_filter(self, filters: SearchFilter) -> None:
         raise NotImplementedError('Not implemented')
      
   @abstractmethod 
   def get_url(self, search: str, filter: Optional[SearchFilter]) -> str:
      raise NotImplementedError('Not implemented')

class SearchStrategy(ABC):
   __website: AnimeWebsite
   
   @abstractmethod
   def execute(self, search: str, filter: Optional[SearchFilter]) -> None:
      raise NotImplementedError('Not implemented')
   
   @abstractmethod
   def request_data(self, url:str) -> None:
      raise NotImplementedError('Not implemented')
   
   @abstractmethod
   def get_result_page(self) -> None:
      raise NotImplementedError('Not implemented')

   @abstractmethod
   def get_result(self) -> None:
      raise NotImplementedError('Not implemented')
