from typing import Dict, Optional
from urllib.parse import urljoin

import aiohttp as aiohttp
import requests as requests

from .client import AspxClient
from .exceptions import ClientError
from .types import ResponseValidationMode


class AsyncAspxClient(AspxClient):
    session: aiohttp.ClientSession

    def __init__(
            self,
            base_uri: str,
            default_headers: Dict[str, str],
            timeout: float,
            response_validation_mode: ResponseValidationMode
    ):
        super().__init__(base_uri, default_headers, timeout, response_validation_mode)
        self.session = aiohttp.ClientSession(headers=default_headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.session.close()

    async def get_aspx_data(self, endpoint: str, params: Optional[Dict[str, Optional[str]]] = None) -> str:
        """
        Fetch raw, unparsed data from a .aspx endpoint
        :param endpoint: (relative) URL of the endpoint
        :param params: query params to send as part of the request
        :return: raw aspx data as a string
        """
        url = urljoin(self.base_uri, endpoint)
        try:
            response = await self.session.get(url, params=params, timeout=self.timeout)

            if response.ok:
                return await response.text()
            else:
                raise ClientError(f'Failed to fetch ASPX data (HTTP/{response.status})')
        except requests.RequestException as e:
            raise ClientError(f'Failed to fetch ASPX data: {e}')
