from abc import ABC, abstractmethod
from utils.Logger import Logger

class IStrategy(ABC):
   @abstractmethod
   def execute(self):
      pass
   @abstractmethod
   def request_data(self):
      pass
   
   @abstractmethod
   def save_to_file(self):
      pass
    