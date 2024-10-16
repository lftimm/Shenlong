import manga_scrapper as msc
from sc_strategies import HTMLScrapper
from utils.Logger import Logger


def main():
    logger = Logger.get_instance()
    err = None
    try:
        html_scrapper = HTMLScrapper()
        scrapper = msc.MangaScrapper(html_scrapper)
        scrapper.scrap()
    except Exception as e:
        err = e 
    finally:
        logger.write(f'Raised a {type(err).__name__}')

if __name__ == '__main__':
   main() 