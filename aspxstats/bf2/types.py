from dataclasses import dataclass
from enum import Enum
from typing import List


class StatsProvider(str, Enum):
    BF2HUB = 'bf2hub'
    PLAYBF2 = 'playbf2'


class SearchMatchType(str, Enum):
    CONTAINS = 'a'
    BEGINS_WITH = 'b'
    ENDS_WITH = 'e'
    EQUALS = 'x'


class SearchSortOrder(str, Enum):
    ASCENDING = 'a'
    DESCENDING = 'r'


@dataclass
class PlayerSearchResult:
    n: int
    pid: int
    nick: str
    score: int

    def __iter__(self):
        yield 'n', self.n
        yield 'pid', self.pid
        yield 'nick', self.nick
        yield 'score', self.score


@dataclass
class PlayerSearchResponse:
    asof: int
    results: List[PlayerSearchResult]

    def __iter__(self):
        yield 'asof', self.asof
        yield 'results', [dict(result) for result in self.results]


class LeaderboardType(str, Enum):
    SCORE = 'score'
    WEAPON = 'weapon'
    VEHICLE = 'vehicle'
    KIT = 'kit'


class ScoreLeaderboardId(str, Enum):
    # Score leaderboards use names as ids
    OVERALL = 'overall'
    RISING_STAR = 'risingstar'
    COMMANDER = 'commander'
    TEAM = 'team'
    COMBAT = 'combat'


class WeaponLeaderboardId(int, Enum):
    ASSAULT_RIFLE = 0
    GRENADE_LAUNCHER = 1
    CARBINE = 2
    LIGHT_MACHINE_GUN = 3
    SNIPER_RIFLE = 4
    PISTOL = 5
    ANTI_TANK = 6
    SUB_MACHINE_GUN = 7
    SHOTGUN = 8
    KNIFE = 9
    DEFIBRILLATOR = 10
    EXPLOSIVES = 11
    GRENADE = 12


class VehicleLeaderboardId(int, Enum):
    ARMOR = 0
    JET = 1
    ANTI_AIR = 2
    HELICOPTER = 3
    TRANSPORT = 4
    GROUND_DEFENSE = 5


class KitLeaderboardId(int, Enum):
    ANTI_TANK = 0
    ASSAULT = 1
    ENGINEER = 2
    MEDIC = 3
    SPEC_OPS = 4
    SUPPORT = 5
    SNIPER = 6


@dataclass
class LeaderboardEntry:
    n: int
    pid: int
    nick: str
    rank: int
    country_code: str

    def __iter__(self):
        yield 'n', self.n
        yield 'pid', self.pid
        yield 'nick', self.nick
        yield 'rank', self.rank
        yield 'country_code', self.country_code


@dataclass
class LeaderboardResponse:
    size: int
    asof: int
    entries: List[LeaderboardEntry]

    def __iter__(self):
        yield 'size', self.size
        yield 'asof', self.asof
        yield 'entries', [dict(entry) for entry in self.entries]


class PlayerinfoKeySet(str, Enum):
    GENERAL_STATS = 'per*,cmb*,twsc,cpcp,cacp,dfcp,kila,heal,rviv,rsup,rpar,tgte,dkas,dsab,cdsc,rank,cmsc,kick,kill,' \
                    'deth,suic,ospm,klpm,klpr,dtpr,bksk,wdsk,bbrs,tcdr,ban,dtpm,lbtl,osaa,vrk,tsql,tsqm,tlwf,mvks,' \
                    'vmks,mvn*,vmr*,fkit,fmap,fveh,fwea,wtm-,wkl-,wdt-,wac-,wkd-,vtm-,vkl-,vdt-,vkd-,vkr-,atm-,awn-,' \
                    'alo-,abr-,ktm-,kkl-,kdt-,kkd-'
    MAP_STATS = 'mtm-,mwn-,mls-'
