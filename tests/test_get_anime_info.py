import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from requests import Response
from search_strategies import MyAnimeListHtmlSearch, MyAnimeListWebsite

class TestMyAnimeListWebsite(unittest.TestCase):
    @patch('search_strategies.requests.get')
    def test_get_anime_info(self, mock_get):
        # Read the local HTML file
        with open('/home/tilt/p/Shenlong/Bleach_ Sennen Kessen-hen (Bleach_ Thousand-Year Blood War) - MyAnimeList.net.html', 'r') as file:
            html_content = file.read()

        # Mock the HTTP response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.content = html_content.encode('utf-8')
        mock_get.return_value = mock_response

        # Create an instance of MyAnimeListWebsite
        search_strategy = MyAnimeListWebsite()

        # Call the get_anime_info method
        result = search_strategy.get_anime_info(mock_response)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result._cover_image, 'https://cdn.myanimelist.net/images/anime/1908/135431.jpg')  
        self.assertEqual(result._title, 'Bleach: Sennen Kessen-hen')  
        self.assertEqual(result._score, '9.01')
        self.assertEqual(result._type, 'TV')   
        self.assertEqual(result._status, 'Finished Airing')
        self.assertEqual(result._studio, 'Pierrot')
        self.assertEqual(result._genres, ['Action', 'Adventure', 'Supernatural'])
        self.assertEqual(result._demographics, 'Shounen')
           
   
        

if __name__ == '__main__':
    unittest.main()
