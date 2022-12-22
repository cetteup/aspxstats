from typing import Dict, Optional, Union

from .schemas import GETLEADERBOARD_RESPONSE_SCHEMA, SEARCHFORPLAYERS_RESPONSE_SCHEMA, \
    GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA, GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA, GETRANKINFO_RESPONSE_SCHEMA, \
    GETAWARDSINFO_RESPONSE_SCHEMA, GETUNLOCKSINFO_RESPONSE_SCHEMA, GETBACKENDINFO_RESPONSE_SCHEMA
from .types import StatsProvider, SearchMatchType, SearchSortOrder, PlayerSearchResponse, LeaderboardType, \
    ScoreLeaderboardId, WeaponLeaderboardId, VehicleLeaderboardId, \
    KitLeaderboardId, LeaderboardResponse, PlayerinfoKeySet, PlayerinfoResponse, \
    PlayerinfoGeneralStats, PlayerinfoMapStats, RankinfoResponse
from ..client import AspxClient as BaseAspxClient
from ..exceptions import InvalidParameterError, InvalidResponseError, NotFoundError
from ..parsing import parse_dict_values
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
        parsed = self.searchforplayers_dict(nick, where, sort)
        return PlayerSearchResponse.from_aspx_response(parsed)

    def searchforplayers_dict(
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
        return self.validate_and_parse_searchforplayers_response(raw_data)

    def validate_and_parse_searchforplayers_response(self, raw_data: str) -> dict:
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

        return self.parse_searchforplayers_response_values(parsed)

    @staticmethod
    def is_valid_searchforplayers_response_data(parsed: dict) -> bool:
        return is_valid_dict(parsed, SEARCHFORPLAYERS_RESPONSE_SCHEMA)

    @staticmethod
    def parse_searchforplayers_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, SEARCHFORPLAYERS_RESPONSE_SCHEMA)

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
        parsed = self.getleaderboard_dict(leaderboard_type, leaderboard_id, pos, before, after, pid)
        return LeaderboardResponse.from_aspx_response(parsed)

    def getleaderboard_dict(
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
            'id': str(leaderboard_id.value),
            'pos': str(pos),
            'before': str(before),
            'after': str(after),
            'pid': str(pid) if pid is not None else None
        })
        return self.validate_and_parse_getleaderboard_response(raw_data)

    def validate_and_parse_getleaderboard_response(self, raw_data: str) -> dict:
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

        return self.parse_getleaderboard_response_values(parsed)

    @staticmethod
    def is_valid_getleaderboard_response_data(parsed: dict) -> bool:
        # TODO: Add per-leaderboard validation with respective attributes
        return is_valid_dict(parsed, GETLEADERBOARD_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getleaderboard_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, GETLEADERBOARD_RESPONSE_SCHEMA)

    def getplayerinfo(
            self,
            pid: int,
            key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS
    ) -> PlayerinfoResponse:
        parsed = self.getplayerinfo_dict(pid, key_set)

        if key_set is PlayerinfoKeySet.GENERAL_STATS:
            data = PlayerinfoGeneralStats.from_aspx_response(parsed)
        else:
            data = PlayerinfoMapStats.from_aspx_response(parsed)

        return PlayerinfoResponse(
            asof=parsed['asof'],
            data=data
        )

    def getplayerinfo_dict(
            self,
            pid: int,
            key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS
    ) -> dict:
        raw_data = self.get_aspx_data('getplayerinfo.aspx', {
            'pid': str(pid),
            'info': key_set
        })
        return self.validate_and_parse_getplayerinfo_response(key_set, raw_data)

    def validate_and_parse_getplayerinfo_response(self, key_set: PlayerinfoKeySet, raw_data: str) -> dict:
        valid_response, not_found = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response and not_found:
            raise NotFoundError(f'No such player on {self.provider}')
        elif not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getplayerinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('data')
        ])

        parsed = self.fix_getplayerinfo_zero_values(parsed)

        valid_data = self.is_valid_getplayerinfo_response_data(key_set, parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getplayerinfo response data')

        return self.parse_getplayerinfo_response_values(key_set, parsed)

    @staticmethod
    def fix_getplayerinfo_zero_values(parsed: dict) -> dict:
        # Can't fix any player attributes if the key is missing/of wrong type
        if not isinstance(parsed.get('data'), dict):
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
            value = parsed['data'].get(key)
            if value is not None and not is_numeric(value):
                parsed['data'][key] = '0'

        return parsed

    @staticmethod
    def is_valid_getplayerinfo_response_data(key_set: PlayerinfoKeySet, parsed: dict) -> bool:
        if key_set is PlayerinfoKeySet.GENERAL_STATS:
            return is_valid_dict(parsed, GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA)
        else:
            return is_valid_dict(parsed, GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getplayerinfo_response_values(key_set: PlayerinfoKeySet, parsed: dict) -> dict:
        if key_set is PlayerinfoKeySet.GENERAL_STATS:
            return parse_dict_values(parsed, GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA)
        else:
            return parse_dict_values(parsed, GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA)

    def getrankinfo(
            self,
            pid: int
    ) -> RankinfoResponse:
        parsed = self.getrankinfo_dict(pid)
        return RankinfoResponse.from_aspx_response(parsed)

    def getrankinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = self.get_aspx_data('getrankinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getrankinfo_response(raw_data)

    def validate_and_parse_getrankinfo_response(self, raw_data: str) -> dict:
        valid_response, not_found = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response and not_found:
            raise NotFoundError(f'No such player on {self.provider}')
        elif not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getrankinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget('data')
        ])

        valid_data = self.is_valid_getrankinfo_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getrankinfo response data')

        return self.parse_getrankinfo_response_values(parsed)

    @staticmethod
    def is_valid_getrankinfo_response_data(parsed: dict) -> bool:
        return is_valid_dict(parsed, GETRANKINFO_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getrankinfo_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, GETRANKINFO_RESPONSE_SCHEMA)

    def getawardsinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = self.get_aspx_data('getawardsinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getawardsinfo_response(raw_data)

    def validate_and_parse_getawardsinfo_response(self, raw_data: str) -> dict:
        valid_response, not_found = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response and not_found:
            raise NotFoundError(f'No such player on {self.provider}')
        elif not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getawardsinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('data', as_list=True)
        ])

        valid_data = self.is_valid_getawardsinfo_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getawardsinfo response data')

        return self.parse_getawardsinfo_response_values(parsed)

    @staticmethod
    def is_valid_getawardsinfo_response_data(parsed: dict) -> bool:
        return is_valid_dict(parsed, GETAWARDSINFO_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getawardsinfo_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, GETAWARDSINFO_RESPONSE_SCHEMA)

    def getunlocksinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = self.get_aspx_data('getunlocksinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getunlocksinfo_response(raw_data)

    def validate_and_parse_getunlocksinfo_response(self, raw_data: str) -> dict:
        valid_response, not_found = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response and not_found:
            raise NotFoundError(f'No such player on {self.provider}')
        elif not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getunlocksinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('status'),
            ParseTarget('data', as_list=True)
        ])

        valid_data = self.is_valid_getunlocksinfo_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getunlocksinfo response data')

        return self.parse_getunlocksinfo_response_values(parsed)

    @staticmethod
    def is_valid_getunlocksinfo_response_data(parsed: dict) -> bool:
        return is_valid_dict(parsed, GETUNLOCKSINFO_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getunlocksinfo_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, GETUNLOCKSINFO_RESPONSE_SCHEMA)

    def getbackendinfo_dict(
            self,
    ) -> dict:
        raw_data = self.get_aspx_data('getbackendinfo.aspx')
        return self.validate_and_parse_getbackendinfo_response(raw_data)

    def validate_and_parse_getbackendinfo_response(self, raw_data: str) -> dict:
        valid_response, _ = self.is_valid_aspx_response(raw_data, self.response_validation_mode)
        if not valid_response:
            raise InvalidResponseError(f'{self.provider} returned an invalid getbackendinfo response')

        parsed = self.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('unlocks', as_list=True)
        ])

        valid_data = self.is_valid_getbackendinfo_response_data(parsed)
        if not valid_data:
            raise InvalidResponseError(f'{self.provider} returned invalid getbackendinfo response data')

        return self.parse_getbackendinfo_response_values(parsed)

    @staticmethod
    def is_valid_getbackendinfo_response_data(parsed: dict) -> bool:
        return is_valid_dict(parsed, GETBACKENDINFO_RESPONSE_SCHEMA)

    @staticmethod
    def parse_getbackendinfo_response_values(parsed: dict) -> dict:
        return parse_dict_values(parsed, GETBACKENDINFO_RESPONSE_SCHEMA)

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
