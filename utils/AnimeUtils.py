from dataclasses import dataclass
from requests import Response
from typing import Optional, List, Callable


@dataclass
class SearchFilter:
    _score: Optional[int] = None
    _type: Optional[str] = None
    _status: Optional[str] = None
    
@dataclass
class AnimeData:
    _cover_image: Optional[str] = None
    _title: Optional[str] = None
    _score: Optional[int] = None
    _type: Optional[str] = None
    _status: Optional[str] = None
    _studio: Optional[str] = None
    _genres: Optional[List[str]] = None
    _demographics: Optional[str] = None