from typing import Union, Optional

from .async_client import AsyncAspxClient
from .types import SearchMatchType, SearchSortOrder, PlayerSearchResponse, StatsProvider, LeaderboardType, \
    ScoreLeaderboardId, WeaponType, VehicleType, KitType, LeaderboardResponse, \
    PlayerinfoKeySet, PlayerinfoResponse, RankinfoResponse
from ..types import ResponseValidationMode


async def async_searchforplayers(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> PlayerSearchResponse:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.searchforplayers(nick, where, sort)


async def async_searchforplayers_dict(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.searchforplayers_dict(nick, where, sort)


async def async_getleaderboard(
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
        pid: Optional[int] = None,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> LeaderboardResponse:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.getleaderboard(leaderboard_type, leaderboard_id, pos, before, after, pid)


async def async_getleaderboard_dict(
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
        pid: Optional[int] = None,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.getleaderboard_dict(leaderboard_type, leaderboard_id, pos, before, after, pid)


async def async_getplayerinfo(
        pid: int,
        key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> PlayerinfoResponse:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.getplayerinfo(pid, key_set)


async def async_getplayerinfo_dict(
        pid: int,
        key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.getplayerinfo_dict(pid, key_set)


async def async_getrankinfo(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> RankinfoResponse:
    async with AsyncAspxClient(provider, timeout, response_validation_mode) as client:
        return await client.getrankinfo(pid)


async def async_getrankinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode) as client:
        return await client.getrankinfo_dict(pid)


async def async_getawardsinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode) as client:
        return await client.getawardsinfo_dict(pid)


async def async_getunlocksinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return await client.getunlocksinfo_dict(pid)


async def async_getbackendinfo_dict(
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    async with AsyncAspxClient(provider, timeout, response_validation_mode) as client:
        return await client.getbackendinfo_dict()
