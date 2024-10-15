import os
from datetime import datetime
from typing import Optional
from enum import Enum

class DateDetails(Enum):
    day_month: int = 1
    hour_minute: int = 2

class Logger:
    __instance = None

    @staticmethod
    def get_instance() -> None:
        if Logger.__instance == None:
            Logger()
        return Logger.__instance 
    
    def __init__(self) -> None:
        if Logger.__instance != None:
            Logger.__instance = Logger()
        else:
            Logger.__instance = self

            self.base_log_dir = 'logs'
            self.file = self.__generate_log_file_name()
            self.path = os.path.join(self.base_log_dir,self.file)
            self.path_exists = os.path.exists(self.path)
            if not self.path_exists:
                os.makedirs('logs')
            
    def write(self,message: str) -> None:
        flag: str = 'a' if self.path_exists else 'w'
        
        with open(self.path, flag) as f:
            f.write(self.__relevant_time(DateDetails.hour_minute)+ ' ' + message + '\n')


    def __relevant_time(self, date_details: DateDetails = DateDetails.day_month,
                              dformat: Optional[str] = '__',
                              hformat: Optional[str] = '[:]') -> str:
        date_today = datetime.today()
        time_now = date_today.strftime(f'{hformat[0]}%H{hformat[1]}%M{hformat[2]}')
        date_today = date_today.strftime(f'%d{dformat}%m')

        if(date_details == DateDetails.day_month):
            return date_today
        else:
            return time_now

    def __generate_log_file_name(self) -> str:
        date_now = self.__relevant_time(DateDetails.day_month)
        log_file_name = f'log_file_{date_now}.txt'

        return log_file_name