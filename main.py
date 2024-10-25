import anime_search as msc
from utils.Logger import Logger
from utils.AnimeUtils import SearchFilter
from search_strategies import MyAnimeListHtmlSearch, MyAnimeListWebsite

def main():
    Logger.clear_file(Logger.get_log_path())
    search_method = MyAnimeListHtmlSearch(MyAnimeListWebsite)
    filter = SearchFilter(_type='tv',_score=8)
    search = msc.AnimeSearch(search_method)
    search.search('One Piece', filter)
    print(search)
    

if __name__ == '__main__':
   main() 