from ..utils.AnimeUtils import SearchFilter
from ..utils.Logger import Logger
from .search_strategies import SearchStrategy

from typing import Optional

class Controller:
   __logger = Logger().get_instance()
   def __init__(self, strategy: SearchStrategy = None):
      self.__strategy: SearchStrategy = strategy
      
   def set_strategy(self, strategy: SearchStrategy):
      self.__strategy = strategy
      AnimeSearch.__logger.write(f'Strategy set to -> {str(strategy)}')
      
   def search(self, title: str, filter: Optional[SearchStrategy] = None) -> bool:
      try:
         Controller.__logger.write(f'Entered the search method with title: {title}')
         if self.__strategy is None:
            AnimeSearch.__logger.write('No strategy was set in AnimeSearch.Search(self)')
            raise ValueError('No strategy set')

         self.__strategy.execute(title, filter)
         self.__strategy.get_result_page()
         
         AnimeSearch.__logger.write('->> End of Execution')
         return True
      except Exception as err:
         self.__logger.write(f'Exception Raised: {err}')
         return False
      
   def get_result(self):
      return self.__strategy.get_result()
   
class AnimeSearch(Controller):
   def __init__(self, strategy: SearchStrategy):
      try:
         logger = Logger.get_instance()
         logger.write(f'-> Start of Execution')
         self.strategy = strategy
         super().__init__(strategy)
      except Exception as err:
         logger.write(f'Excpetion Raised: {err}')
   
   def get_result(self):
      return super().get_result()
   
   def __str__(self) -> str:
      return super().get_result()