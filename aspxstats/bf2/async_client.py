from typing import Optional, Union

from .client import AspxClient
from .types import StatsProvider, SearchMatchType, SearchSortOrder, PlayerSearchResponse, LeaderboardType, \
    ScoreLeaderboardId, WeaponType, VehicleType, \
    KitType, LeaderboardResponse, PlayerinfoKeySet, PlayerinfoResponse, \
    PlayerinfoGeneralStats, PlayerinfoMapStats, RankinfoResponse
from ..async_client import AsyncAspxClient as AsyncBaseAspxClient
from ..types import ResponseValidationMode


class AsyncAspxClient(AspxClient, AsyncBaseAspxClient):
    provider: StatsProvider

    def __init__(
            self,
            provider: StatsProvider = StatsProvider.BF2HUB,
            timeout: float = 2.0,
            response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
            clean_nicks: bool = False,
    ):
        super().__init__(provider, timeout, response_validation_mode, clean_nicks)

    async def searchforplayers(
            self,
            nick: str,
            where: SearchMatchType = SearchMatchType.EQUALS,
            sort: SearchSortOrder = SearchSortOrder.ASCENDING
    ) -> PlayerSearchResponse:
        parsed = await self.searchforplayers_dict(nick, where, sort)
        return PlayerSearchResponse.from_aspx_response(parsed)

    async def searchforplayers_dict(
            self,
            nick: str,
            where: SearchMatchType = SearchMatchType.EQUALS,
            sort: SearchSortOrder = SearchSortOrder.ASCENDING
    ) -> dict:
        raw_data = await self.get_aspx_data('searchforplayers.aspx', {
            'nick': nick,
            'where': where,
            'sort': sort
        })
        return self.validate_and_parse_searchforplayers_response(raw_data)

    async def getleaderboard(
            self,
            leaderboard_type: LeaderboardType = LeaderboardType.SCORE,
            leaderboard_id: Union[
                ScoreLeaderboardId,
                WeaponType,
                VehicleType,
                KitType
            ] = ScoreLeaderboardId.OVERALL,
            pos: int = 1,
            before: int = 0,
            after: int = 19,
            pid: Optional[int] = None
    ) -> LeaderboardResponse:
        parsed = await self.getleaderboard_dict(leaderboard_type, leaderboard_id, pos, before, after, pid)
        return LeaderboardResponse.from_aspx_response(parsed)

    async def getleaderboard_dict(
            self,
            leaderboard_type: LeaderboardType = LeaderboardType.SCORE,
            leaderboard_id: Union[
                ScoreLeaderboardId,
                WeaponType,
                VehicleType,
                KitType
            ] = ScoreLeaderboardId.OVERALL,
            pos: int = 1,
            before: int = 0,
            after: int = 19,
            pid: Optional[int] = None
    ) -> dict:
        # TODO Validate type and id combinations
        raw_data = await self.get_aspx_data('getleaderboard.aspx', {
            'type': leaderboard_type,
            'id': str(leaderboard_id.value),
            'pos': str(pos),
            'before': str(before),
            'after': str(after),
            'pid': str(pid) if pid is not None else None
        })
        return self.validate_and_parse_getleaderboard_response(raw_data)

    async def getplayerinfo(
            self,
            pid: int,
            key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS
    ) -> PlayerinfoResponse:
        parsed = await self.getplayerinfo_dict(pid, key_set)

        if key_set is PlayerinfoKeySet.GENERAL_STATS:
            data = PlayerinfoGeneralStats.from_aspx_response(parsed)
        else:
            data = PlayerinfoMapStats.from_aspx_response(parsed)

        return PlayerinfoResponse(
            asof=parsed['asof'],
            data=data
        )

    async def getplayerinfo_dict(
            self,
            pid: int,
            key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS
    ) -> dict:
        raw_data = await self.get_aspx_data('getplayerinfo.aspx', {
            'pid': str(pid),
            'info': key_set
        })
        return self.validate_and_parse_getplayerinfo_response(key_set, raw_data)

    async def getrankinfo(
            self,
            pid: int
    ) -> RankinfoResponse:
        parsed = await self.getrankinfo_dict(pid)
        return RankinfoResponse.from_aspx_response(parsed)

    async def getrankinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = await self.get_aspx_data('getrankinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getrankinfo_response(raw_data)

    async def getawardsinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = await self.get_aspx_data('getawardsinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getawardsinfo_response(raw_data)

    async def getunlocksinfo_dict(
            self,
            pid: int
    ) -> dict:
        raw_data = await self.get_aspx_data('getunlocksinfo.aspx', {
            'pid': str(pid)
        })
        return self.validate_and_parse_getunlocksinfo_response(raw_data)

    async def getbackendinfo_dict(
            self,
    ) -> dict:
        raw_data = await self.get_aspx_data('getbackendinfo.aspx')
        return self.validate_and_parse_getbackendinfo_response(raw_data)
