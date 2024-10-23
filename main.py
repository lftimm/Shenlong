import anime_search as msc
from utils.SearchFilter import SearchFilter
from search_strategies import MyAnimeListHtmlSearch

def main():
    search_method = MyAnimeListHtmlSearch()
    filter = SearchFilter(_type='tv',_score=8)
    scrapper = msc.AnimeSearch(search_method)
    scrapper.search('Bleach', filter)

if __name__ == '__main__':
   main() 