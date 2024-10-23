import os
from datetime import datetime
from typing import Optional
from enum import Enum

class DateDetails(Enum):
    day_month: int = 1
    hour_minute: int = 2

def _relevant_time(date_details: DateDetails = DateDetails.day_month,
                   dformat: Optional[str] = '__',
                   hformat: Optional[str] = '[:]') -> str:
    
    date_today = datetime.today()
    time_now = date_today.strftime(f'{hformat[0]}%H{hformat[1]}%M{hformat[2]}')
    date_today = date_today.strftime(f'%d{dformat}%m')

    if(date_details == DateDetails.day_month):
        return date_today
    else:
        return time_now

class Logger:
    _instance = None

    def __init__(self) -> None:
        if Logger._instance is not None:
            raise Exception("Logger can only be instantiated once.")
        else:
            Logger._instance = self

            self.base_log_dir = 'logs'
            self.file = self.__generate_log_file_name()
            self.path = os.path.join(self.base_log_dir,self.file)
            
            if not os.path.exists(self.base_log_dir):
                os.makedirs(self.base_log_dir)
    
    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance 
         
            
    def write(self, message: str) -> None:
        flag: str = 'a' if os.path.exists(self.path) else 'w'
        
        with open(self.path, flag) as f:
            f.write(_relevant_time(DateDetails.hour_minute)+ ' ' + message + '\n')

    def __generate_log_file_name(self) -> str:
        date_now = _relevant_time(DateDetails.day_month)
        log_file_name = f'log_file_{date_now}.txt'

        return log_file_name
    