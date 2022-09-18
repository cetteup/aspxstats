from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ProviderConfig:
    base_uri: str
    default_headers: Optional[Dict[str, str]] = None
