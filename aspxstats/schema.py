from dataclasses import dataclass
from typing import Optional, Dict, Union, TypeVar


@dataclass
class AttributeSchema:
    type: type
    is_numeric: bool = False
    is_booly: bool = False
    is_floaty: bool = False
    is_ratio: bool = False
    is_nick: bool = False
    children: Optional[Dict[str, Union[dict, 'AttributeSchema']]] = None


DictSchema = TypeVar('DictSchema', bound=Dict[str, Union[dict, AttributeSchema]])
