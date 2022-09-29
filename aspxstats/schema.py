from dataclasses import dataclass
from typing import Optional, Dict, Union


@dataclass
class AttributeSchema:
    type: type
    is_numeric: bool = False
    is_floaty: bool = False
    is_ratio: bool = False
    children: Optional[Dict[str, Union[dict, 'AttributeSchema']]] = None
