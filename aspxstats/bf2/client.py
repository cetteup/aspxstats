from typing import Dict, Optional, Union

from .schemas import GETLEADERBOARD_RESPONSE_SCHEMA, SEARCHFORPLAYERS_RESPONSE_SCHEMA
from ..client import AspxClient as BaseAspxClient
from ..exceptions import InvalidParameterError, InvalidResponseError
from ..types import ProviderConfig, ParseTarget
from ..validation import AttributeSchema, is_valid_dict
from .types import StatsProvider, SearchMatchType, SearchSortOrder, PlayerSearchResult, \
    PlayerSearchResponse, LeaderboardType, ScoreLeaderboardId, WeaponLeaderboardId, VehicleLeaderboardId, \
    KitLeaderboardId, LeaderboardEntry, LeaderboardResponse


class AspxClient(BaseAspxClient):
    provider: StatsProvider

    def __init__(self, provider: StatsProvider = StatsProvider.BF2HUB, timeout: float = 2.0):
        provider_config = AspxClient.get_provider_config(provider)
        super().__init__(provider_config.base_uri, provider_config.default_headers, timeout)
        self.provider = provider

    def searchforplayers(
            self,
            nick: str,
            where: SearchMatchType = SearchMatchType.EQUALS,
            sort: SearchSortOrder = SearchSortOrder.ASCENDING
    ) -> PlayerSearchResponse:
        parsed = self.searchforplayers_raw(nick, where, sort)

        # We can safely access keys and parse integers directly here,
        # since we already validated all used are present and all relevant strings are numeric
        return PlayerSearchResponse(
            asof=int(parsed['asof']),
            results=[
                PlayerSearchResult(
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
            where: SearchMatchType = SearchMatchType.EQUALS,
            sort: SearchSortOrder = SearchSortOrder.ASCENDING
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
        return is_valid_dict(parsed, SEARCHFORPLAYERS_RESPONSE_SCHEMA)

    def getleaderboard(
            self,
            leaderboard_type: LeaderboardType = LeaderboardType.SCORE,
            leaderboard_id: Union[
                ScoreLeaderboardId,
                WeaponLeaderboardId,
                VehicleLeaderboardId,
                KitLeaderboardId
            ] = ScoreLeaderboardId.OVERALL,
            pos: int = 1,
            before: int = 0,
            after: int = 19,
            pid: Optional[int] = None
    ) -> LeaderboardResponse:
        parsed = self.getleaderboard_raw(leaderboard_type, leaderboard_id, pos, before, after, pid)

        return LeaderboardResponse(
            size=int(parsed['size']),
            asof=int(parsed['asof']),
            entries=[
                LeaderboardEntry(
                    n=int(entry['n']),
                    pid=int(entry['pid']),
                    nick=entry['nick'],
                    rank=int(entry['playerrank']),
                    country_code=entry['countrycode']
                ) for entry in parsed['entries']
            ]
        )

    def getleaderboard_raw(
            self,
            leaderboard_type: LeaderboardType = LeaderboardType.SCORE,
            leaderboard_id: Union[
                ScoreLeaderboardId,
                WeaponLeaderboardId,
                VehicleLeaderboardId,
                KitLeaderboardId
            ] = ScoreLeaderboardId.OVERALL,
            pos: int = 1,
            before: int = 0,
            after: int = 19,
            pid: Optional[int] = None
    ) -> dict:
        # TODO Validate type and id combinations
        raw_data = self.get_aspx_data('getleaderboard.aspx', {
            'type': leaderboard_type,
            'id': leaderboard_id,
            'pos': pos,
            'before': before,
            'after': after,
            'pid': pid
        })

        valid_response, _ = self.is_valid_aspx_response(raw_data)
        if not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getleaderboard response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('entries', as_list=True)
        ])

        valid_data = self.is_valid_getleaderboard_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getleaderboard response data')

        return parsed

    @staticmethod
    def is_valid_getleaderboard_response_data(parsed: dict) -> bool:
        # TODO: Add per-leaderboard validation with respective attributes
        return is_valid_dict(parsed, GETLEADERBOARD_RESPONSE_SCHEMA)

    @staticmethod
    def get_provider_config(provider: StatsProvider = StatsProvider.BF2HUB) -> ProviderConfig:
        provider_configs: Dict[StatsProvider, ProviderConfig] = {
            StatsProvider.BF2HUB: ProviderConfig(
                base_uri='http://official.ranking.bf2hub.com/ASP/',
                default_headers={
                    'Host': 'BF2web.gamespy.com',
                    'User-Agent': 'GameSpyHTTP/1.0'
                }
            ),
            StatsProvider.PLAYBF2: ProviderConfig(
                base_uri='http://bf2web.playbf2.ru/ASP/'
            )
        }

        config = provider_configs.get(provider, None)
        if config is None:
            raise InvalidParameterError(f'No provider config for given provider "{provider}"')

        return config
