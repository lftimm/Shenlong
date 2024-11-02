import Shenlong
from Shenlong import MyAnimeListHtmlSearch, MyAnimeListWebsite, SearchFilter

s = Shenlong.search(MyAnimeListHtmlSearch(MyAnimeListWebsite), 'Naruto', SearchFilter(_score=8.0))
