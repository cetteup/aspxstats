from typing import Union, Optional

from .client import AspxClient
from .types import SearchMatchType, SearchSortOrder, PlayerSearchResponse, StatsProvider, LeaderboardType, \
    ScoreLeaderboardId, WeaponType, VehicleType, KitType, LeaderboardResponse, \
    PlayerinfoKeySet, PlayerinfoResponse, RankinfoResponse
from ..types import ResponseValidationMode


def searchforplayers(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> PlayerSearchResponse:
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.searchforplayers(nick, where, sort)


def searchforplayers_dict(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.searchforplayers_dict(nick, where, sort)


def getleaderboard(
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
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.getleaderboard(leaderboard_type, leaderboard_id, pos, before, after, pid)


def getleaderboard_dict(
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
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.getleaderboard_dict(leaderboard_type, leaderboard_id, pos, before, after, pid)


def getplayerinfo(
        pid: int,
        key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> PlayerinfoResponse:
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.getplayerinfo(pid, key_set)


def getplayerinfo_dict(
        pid: int,
        key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.getplayerinfo_dict(pid, key_set)


def getrankinfo(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> RankinfoResponse:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getrankinfo(pid)


def getrankinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getrankinfo_dict(pid)


def getawardsinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getawardsinfo_dict(pid)


def getunlocksinfo_dict(
        pid: int,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX,
        clean_nicks: bool = False
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode, clean_nicks) as client:
        return client.getunlocksinfo_dict(pid)


def getbackendinfo_dict(
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getbackendinfo_dict()
