from dataclasses import dataclass
from enum import Enum
from typing import List, Union


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


@dataclass
class PlayerinfoTimestamps:
    joined: int
    last_battle: int

    def __iter__(self):
        yield 'joined', self.joined
        yield 'last_battle', self.last_battle


@dataclass
class PlayerinfoScores:
    total: int
    teamwork: int
    combat: int
    commander: int
    best_round: int
    per_minute: int

    def __iter__(self):
        yield 'total', self.total
        yield 'teamwork', self.teamwork
        yield 'combat', self.combat
        yield 'commander', self.commander
        yield 'best_round', self.best_round
        yield 'per_minute', self.per_minute


@dataclass
class PlayerinfoTeamwork:
    flag_captures: int
    flag_assists: int
    flag_defends: int
    kill_assists: int
    target_assists: int
    heals: int
    revives: int
    resupplies: int
    repairs: int
    driver_assists: int
    driver_specials: int

    def __iter__(self):
        yield 'flag_captures', self.flag_captures
        yield 'flag_assists', self.flag_assists
        yield 'flag_defends', self.flag_defends
        yield 'kill_assists', self.kill_assists
        yield 'target_assists', self.target_assists
        yield 'heals', self.heals
        yield 'revives', self.revives
        yield 'resupplies', self.resupplies
        yield 'repairs', self.repairs
        yield 'driver_assists', self.driver_assists
        yield 'driver_specials', self.driver_specials


@dataclass
class PlayerinfoTimes:
    total: int
    commander: int
    squad_leader: int
    squad_member: int
    lone_wolf: int

    def __iter__(self):
        yield 'total', self.total
        yield 'commander', self.commander
        yield 'squad_leader', self.squad_leader
        yield 'squad_member', self.squad_member
        yield 'lone_wolf', self.lone_wolf


@dataclass
class PlayerinfoRounds:
    conquest: int
    supply_lines: int
    coop: int
    wins: int
    losses: int

    def __iter__(self):
        yield 'conquest', self.conquest
        yield 'supply_lines', self.supply_lines
        yield 'coop', self.coop
        yield 'wins', self.wins
        yield 'losses', self.losses


@dataclass
class PlayerinfoKills:
    total: int
    streak: int
    per_minute: float
    per_round: float

    def __iter__(self):
        yield 'total', self.total
        yield 'streak', self.streak
        yield 'per_minute', self.per_minute
        yield 'per_round', self.per_round


@dataclass
class PlayerinfoDeaths:
    total: int
    suicides: int
    streak: int
    per_minute: float
    per_round: float

    def __iter__(self):
        yield 'total', self.total
        yield 'suicides', self.suicides
        yield 'streak', self.streak
        yield 'per_minute', self.per_minute
        yield 'per_round', self.per_round


@dataclass
class PlayerinfoFavorites:
    kit: int
    weapon: int
    vehicle: int
    map: int

    def __iter__(self):
        yield 'kit', self.kit
        yield 'weapon', self.weapon
        yield 'vehicle', self.vehicle
        yield 'map', self.map


@dataclass
class PlayerinfoWeapon:
    id: int
    time: int
    kills: int
    deaths: int
    accuracy: float
    kd: float

    def __iter__(self):
        yield 'id', self.id
        yield 'time', self.time
        yield 'kills', self.kills
        yield 'deaths', self.deaths
        yield 'accuracy', self.accuracy
        yield 'kd', self.kd


@dataclass
class PlayerinfoVehicle:
    id: int
    time: int
    kills: int
    deaths: int
    kd: float
    road_kills: int

    def __iter__(self):
        yield 'id', self.id
        yield 'time', self.time
        yield 'kills', self.kills
        yield 'deaths', self.deaths
        yield 'kd', self.kd
        yield 'road_kills', self.road_kills


@dataclass
class PlayerinfoArmy:
    id: int
    time: int
    wins: int
    losses: int
    best_round_score: int

    def __iter__(self):
        yield 'id', self.id
        yield 'time', self.time
        yield 'wins', self.wins
        yield 'losses', self.losses
        yield 'best_round_score', self.best_round_score


@dataclass
class PlayerinfoKit:
    id: int
    time: int
    kills: int
    deaths: int
    kd: float

    def __iter__(self):
        yield 'id', self.id
        yield 'time', self.time
        yield 'kills', self.kills
        yield 'deaths', self.deaths
        yield 'kd', self.kd


@dataclass
class PlayerinfoTactical:
    teargas_flashbang_deploys: int
    grappling_hook_deploys: int
    zipline_deploys: int

    def __iter__(self):
        yield 'teargas_flashbang_deploys', self.teargas_flashbang_deploys
        yield 'grappling_hook_deploys', self.grappling_hook_deploys
        yield 'zipline_deploys', self.zipline_deploys


@dataclass
class PlayerinfoRelation:
    pid: int
    nick: str
    rank: int
    kills: int

    def __iter__(self):
        yield 'pid', self.pid
        yield 'nick', self.nick
        yield 'rank', self.rank
        yield 'kills', self.kills


@dataclass
class PlayerinfoRelations:
    top_rival: PlayerinfoRelation
    top_victim: PlayerinfoRelation

    def __iter__(self):
        yield 'top_rival', dict(self.top_rival)
        yield 'top_victim', dict(self.top_victim)


@dataclass
class PlayerinfoGeneralStats:
    pid: int
    nick: str
    rank: int
    sgt_major_of_the_corps: bool
    times_kicked: int
    times_banned: int
    accuracy: float
    timestamp: PlayerinfoTimestamps
    score: PlayerinfoScores
    time: PlayerinfoTimes
    rounds: PlayerinfoRounds
    kills: PlayerinfoKills
    deaths: PlayerinfoDeaths
    teamwork: PlayerinfoTeamwork
    tactical: PlayerinfoTactical
    favorite: PlayerinfoFavorites
    weapons: List[PlayerinfoWeapon]
    vehicles: List[PlayerinfoVehicle]
    armies: List[PlayerinfoArmy]
    kits: List[PlayerinfoKit]
    relations: PlayerinfoRelations

    def __iter__(self):
        yield 'pid', self.pid
        yield 'nick', self.nick
        yield 'rank', self.rank
        yield 'sgt_major_of_the_corps', self.sgt_major_of_the_corps
        yield 'times_kicked', self.times_kicked
        yield 'times_banned', self.times_banned
        yield 'accuracy', self.accuracy
        yield 'timestamp', dict(self.timestamp)
        yield 'score', dict(self.score)
        yield 'time', dict(self.time)
        yield 'rounds', dict(self.rounds)
        yield 'kills', dict(self.kills)
        yield 'deaths', dict(self.deaths)
        yield 'teamwork', dict(self.teamwork)
        yield 'tactical', dict(self.tactical)
        yield 'favorite', dict(self.favorite)
        yield 'weapons', [dict(w) for w in self.weapons]
        yield 'vehicles', [dict(v) for v in self.vehicles]
        yield 'armies', [dict(a) for a in self.armies]
        yield 'kits', [dict(k) for k in self.kits]
        yield 'relations', dict(self.relations)


@dataclass
class PlayerinfoMap:
    id: int
    time: int
    wins: int
    losses: int

    def __iter__(self):
        yield 'id', self.id
        yield 'time', self.time
        yield 'wins', self.wins
        yield 'losses', self.losses


@dataclass
class PlayerinfoMapStats:
    pid: int
    nick: str
    maps: List[PlayerinfoMap]

    def __iter__(self):
        yield 'pid', self.pid
        yield 'nick', self.nick
        yield 'maps', [dict(m) for m in self.maps]


@dataclass
class PlayerinfoResponse:
    asof: int
    data: Union[PlayerinfoGeneralStats, PlayerinfoMapStats]

    def __iter__(self):
        yield 'asof', self.asof
        yield 'data', dict(self.data)
