from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from .client import AspxClient, ParseTarget
from .common import ProviderConfig
from .exceptions import InvalidParameterError, InvalidResponseError


class Bf2StatsProvider(str, Enum):
    BF2HUB = 'bf2hub'
    PLAYBF2 = 'playbf2'


class Bf2SearchMatchType(str, Enum):
    CONTAINS = 'a'
    BEGINS_WITH = 'b'
    ENDS_WITH = 'e'
    EQUALS = 'x'


class Bf2SearchSortOrder(str, Enum):
    ASCENDING = 'a'
    DESCENDING = 'r'


@dataclass
class Bf2PlayerSearchResult:
    n: int
    pid: int
    nick: str
    score: int


@dataclass
class Bf2PlayerSearchResponse:
    asof: int
    results: List[Bf2PlayerSearchResult]


class Bf2AspxClient(AspxClient):
    provider: Bf2StatsProvider

    def __init__(self, provider: Bf2StatsProvider = Bf2StatsProvider.BF2HUB, timeout: float = 2.0):
        provider_config = Bf2AspxClient.get_provider_config(provider)
        super().__init__(provider_config.base_uri, provider_config.default_headers, timeout)
        self.provider = provider

    def searchforplayers(
            self,
            nick: str,
            where: Bf2SearchMatchType = Bf2SearchMatchType.EQUALS,
            sort: Bf2SearchSortOrder = Bf2SearchSortOrder.ASCENDING
    ) -> Bf2PlayerSearchResponse:
        parsed = self.searchforplayers_raw(nick, where, sort)

        # We can safely access keys and parse integers directly here,
        # since we already validated all used are present and all relevant strings are numeric
        return Bf2PlayerSearchResponse(
            asof=int(parsed['asof']),
            results=[
                Bf2PlayerSearchResult(
                    n=int(result['n']),
                    nick=result['nick'],
                    pid=int(result['pid']),
                    score=int(result['score'])
                ) for result in parsed['results']
            ]
        )

    def searchforplayers_raw(
            self,
            nick: str,
            where: Bf2SearchMatchType = Bf2SearchMatchType.EQUALS,
            sort: Bf2SearchSortOrder = Bf2SearchSortOrder.ASCENDING
    ) -> dict:
        raw_data = self.get_aspx_data('searchforplayers.aspx', {
            'nick': nick,
            'where': where,
            'sort': sort
        })

        valid_response, _ = self.is_valid_aspx_response(raw_data)
        if not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid searchforplayers response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('results', as_list=True)
        ])

        valid_data = self.is_valid_searchforplayers_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid searchforplayers response data')

        return parsed

    @staticmethod
    def is_valid_searchforplayers_response_data(parsed: dict) -> bool:
        # Check if "asof" is present and is a numeric string
        if not isinstance(parsed.get('asof'), str) or not parsed['asof'].isnumeric():
            return False

        # Check if "results" is present and is a list
        if not isinstance(parsed.get('results'), list):
            return False

        # Check if all elements in "results" are dictionaries with the required keys and values of type str
        return all(
            isinstance(result, dict) and
            Bf2AspxClient.is_valid_searchforplayers_result_data(result) for result in parsed['results']
        )

    @staticmethod
    def is_valid_searchforplayers_result_data(result: dict) -> bool:
        # Check if nick is present and is a string
        if not isinstance(result.get('nick'), str):
            return False

        # Check if n, nick and score are presnet and are numeric strings
        return all(isinstance(result.get(key), str) and result.get(key).isnumeric() for key in ['n', 'pid', 'score'])

    @staticmethod
    def get_provider_config(provider: Bf2StatsProvider = Bf2StatsProvider.BF2HUB) -> ProviderConfig:
        provider_configs: Dict[Bf2StatsProvider, ProviderConfig] = {
            Bf2StatsProvider.BF2HUB: ProviderConfig(
                base_uri='http://official.ranking.bf2hub.com/ASP/',
                default_headers={
                    'Host': 'BF2web.gamespy.com',
                    'User-Agent': 'GameSpyHTTP/1.0'
                }
            ),
            Bf2StatsProvider.PLAYBF2: ProviderConfig(
                base_uri='http://bf2web.playbf2.ru/ASP/'
            )
        }

        config = provider_configs.get(provider, None)
        if config is None:
            raise InvalidParameterError(f'No provider config for given provider "{provider}"')

        return config
