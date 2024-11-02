from ..utils.AnimeUtils import SearchFilter
from ..search.anime_search import AnimeSearch
from ..utils.project_abcs import SearchStrategy
from ..utils.Logger import Logger

def search(search_method: SearchStrategy, title: str, filter: SearchFilter):
    logger = Logger.get_instance()
    logger.clear_file(logger.get_log_path())
    search = AnimeSearch(search_method)
    return_value: bool = search.search(title, filter)
    if return_value is True:
        return search.get_result()
    else:
        logger.write(f'Search Failed, raised exception.')
        raise Exception('Search Failed')

