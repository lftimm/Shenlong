from utils.Logger import Logger
from project_abcs import SearchStrategy
from typing import Optional

class Controller:
   __logger = Logger().get_instance()
   def __init__(self, strategy: SearchStrategy = None):
      self.__strategy: SearchStrategy = strategy
      
   def set_strategy(self, strategy: SearchStrategy):
      self.__strategy = strategy
      AnimeSearch.__logger.write(f'Strategy set to -> {str(strategy)}')
      
   def search(self, title: str, filter: Optional[SearchStrategy] = None) -> bool:
      Controller.__logger.write(f'Entered the search method with title: {title}')
      if self.__strategy is None:
         AnimeSearch.__logger.write('No strategy was set in AnimeSearch.Search(self)')
         raise ValueError('No strategy set')

      self.__strategy.execute(title, filter)
      self.__strategy.get_result_page()
      
      AnimeSearch.__logger.write('->> End of Execution')
      return True
   
   def get_reusult(self):
      return self.__strategy.get_result()
   
   def __str__(self):
      return str(self.__strategy.get_result())
   
   
class AnimeSearch(Controller):
   def __init__(self, strategy: SearchStrategy):
      try:
         logger = Logger.get_instance()
         logger.write(f'-> Start of Execution')
         super().__init__(strategy)
      except Exception as err:
         logger.write(f'Excpetion Raised: {err}')