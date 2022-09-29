from typing import Union, Optional

from .client import AspxClient
from .types import SearchMatchType, SearchSortOrder, PlayerSearchResponse, StatsProvider, LeaderboardType, \
    ScoreLeaderboardId, WeaponLeaderboardId, VehicleLeaderboardId, KitLeaderboardId, LeaderboardResponse, \
    PlayerinfoKeySet
from ..types import ResponseValidationMode


def searchforplayers(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> PlayerSearchResponse:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.searchforplayers(nick, where, sort)


def searchforplayers_raw(
        nick: str,
        where: SearchMatchType = SearchMatchType.EQUALS,
        sort: SearchSortOrder = SearchSortOrder.ASCENDING,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.searchforplayers_raw(nick, where, sort)


def getleaderboard(
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
        pid: Optional[int] = None,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> LeaderboardResponse:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getleaderboard(leaderboard_type, leaderboard_id, pos, before, after, pid)


def getleaderboard_raw(
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
        pid: Optional[int] = None,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getleaderboard_raw(leaderboard_type, leaderboard_id, pos, before, after, pid)


def getplayerinfo_raw(
        pid: int,
        key_set: PlayerinfoKeySet = PlayerinfoKeySet.GENERAL_STATS,
        provider: StatsProvider = StatsProvider.BF2HUB,
        timeout: float = 2.0,
        response_validation_mode: ResponseValidationMode = ResponseValidationMode.LAX
) -> dict:
    with AspxClient(provider, timeout, response_validation_mode) as client:
        return client.getplayerinfo_raw(pid, key_set)
