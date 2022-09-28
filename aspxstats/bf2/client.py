from typing import Dict, Optional, Union

from .schemas import GETLEADERBOARD_RESPONSE_SCHEMA, SEARCHFORPLAYERS_RESPONSE_SCHEMA, \
    GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA, GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA
from .types import StatsProvider, SearchMatchType, SearchSortOrder, PlayerSearchResult, \
    PlayerSearchResponse, LeaderboardType, ScoreLeaderboardId, WeaponLeaderboardId, VehicleLeaderboardId, \
    KitLeaderboardId, LeaderboardEntry, LeaderboardResponse, PlayerinfoKeySet
from ..client import AspxClient as BaseAspxClient
from ..exceptions import InvalidParameterError, InvalidResponseError, NotFoundError
from ..types import ProviderConfig, ParseTarget, ResponseValidationMode
from ..validation import is_valid_dict, is_numeric


class AspxClient(BaseAspxClient):
    provider: StatsProvider

    def __init__(
            self,
            provider: StatsProvider = StatsProvider.BF2HUB,
            timeout: float = 2.0,
            response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
    ):
        provider_config = AspxClient.get_provider_config(provider)
        super().__init__(provider_config.base_uri, provider_config.default_headers, timeout, response_validation_mode)
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

        valid_response, _ = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
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

        valid_response, _ = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
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

    def getplayerinfo_raw(
            self,
            pid: int,
            key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS
    ) -> dict:
        raw_data = self.get_aspx_data('getplayerinfo.aspx', {
            'pid': pid,
            'info': key_set
        })

        valid_response, not_found = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response and not_found:
            raise NotFoundError(f'No such player on {self.provider}')
        elif not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getplayerinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('player')
        ])

        parsed = self.fix_getplayerinfo_zero_values(parsed)

        valid_data = self.is_valid_getplayerinfo_response_data(key_set, parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getplayerinfo response data')

        return parsed

    @staticmethod
    def fix_getplayerinfo_zero_values(parsed: dict) -> dict:
        # Can't fix any player attributes if the key is missing/of wrong type
        if not isinstance(parsed.get('player'), dict):
            return parsed

        """
        If a player has no kills/deaths, the PlayBF2 backend returns
        a whitespace instead of a zero integer value for:
        tvcr (top victim pid)
        topr (top opponent pid)
        mvrs (top victim rank)
        vmrs (top opponent rank)
        BF2Hub handles it better in most cases, but also has players with an empty string mvrs/vmrs or even more
        interesting values such as "NOT VAILABLE" for tvcr (pid 10226681 asof 1617839795)
        => replace any invalid values with 0 (but don't add it if the key is missing)
        """
        for key in ['tvcr', 'topr', 'mvrs', 'vmrs']:
            value = parsed['player'].get(key)
            if value is not None and not is_numeric(value):
                parsed['player'][key] = '0'

        return parsed

    @staticmethod
    def is_valid_getplayerinfo_response_data(key_set: PlayerinfoKeySet, parsed: dict) -> bool:
        if key_set == PlayerinfoKeySet.GENERAL_STATS:
            return is_valid_dict(parsed, GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA)
        else:
            return is_valid_dict(parsed, GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA)

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
