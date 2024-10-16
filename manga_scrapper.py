from utils.Logger import Logger
from utils.IStrategy import IStrategy

class MangaScrapper:
   __logger = Logger().get_instance()
   def __init__(self, strategy: IStrategy = None):
      self.__strategy: IStrategy = strategy
      
   def set_strategy(self, strategy: IStrategy):
      self.__strategy = strategy
      MangaScrapper.__logger.write(f'Strategy set to -> {str(strategy)}')
      
   def scrap(self):
      if self.__strategy is None:
         try:
            MangaScrapper.__logger.write('No strategy was set in MangaScrapper.scrap(self)')
            raise ValueError('No strategy set')
         except ValueError as err:
            logger = Logger.get_instance()
            logger.write(err)
            
      MangaScrapper.__logger.write('No strategy was set in MangaScrapper.scrap(self)')
      self.__strategy.execute()