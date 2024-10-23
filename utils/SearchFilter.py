from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchFilter:
    _score: Optional[int] = None
    _type: Optional[str] = None
    _status: Optional[str] = None