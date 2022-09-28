from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Optional, Dict, List


@dataclass
class ProviderConfig:
    base_uri: str
    default_headers: Optional[Dict[str, str]] = None


class ResponseValidationMode(IntEnum):
    LAX = 0
    STRICT = 1


class LineType(str, Enum):
    HEADERS = 'header'
    DATA = 'data'


class Dataset:
    keys: str
    data: List[str]

    def __init__(self, keys: str):
        self.keys = keys
        self.data = []


class ParseTarget:
    to_key: str
    as_list: bool
    to_root: bool

    def __init__(self, to_key: str = '', as_list: bool = False, to_root: bool = False):
        self.to_key = to_key
        self.as_list = as_list
        self.to_root = to_root
