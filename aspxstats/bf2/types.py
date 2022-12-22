from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from .utils import group_stats_by_item


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

    @staticmethod
    def from_aspx_response(parsed: dict) -> 'PlayerSearchResponse':
        return PlayerSearchResponse(
            asof=parsed['asof'],
            results=[
                PlayerSearchResult(
                    n=result['n'],
                    nick=result['nick'],
                    pid=result['pid'],
                    score=result['score']
                ) for result in parsed['results']
            ]
        )


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

    @staticmethod
    def from_aspx_response(parsed: dict) -> 'LeaderboardResponse':
        return LeaderboardResponse(
            size=parsed['size'],
            asof=parsed['asof'],
            entries=[
                LeaderboardEntry(
                    n=entry['n'],
                    pid=entry['pid'],
                    nick=entry['nick'],
                    rank=entry['playerrank'],
                    country_code=entry['countrycode']
                ) for entry in parsed['entries']
            ]
        )


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
    per_minute: float

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

    @staticmethod
    def from_aspx_response(parsed: dict) -> 'PlayerinfoGeneralStats':
        return PlayerinfoGeneralStats(
            pid=parsed['data']['pid'],
            nick=parsed['data']['nick'],
            rank=parsed['data']['rank'],
            sgt_major_of_the_corps=parsed['data']['smoc'],
            times_kicked=parsed['data']['kick'],
            times_banned=parsed['data']['ban'],
            accuracy=parsed['data']['osaa'],
            timestamp=PlayerinfoTimestamps(
                joined=parsed['data']['jond'],
                last_battle=parsed['data']['lbtl']
            ),
            score=PlayerinfoScores(
                total=parsed['data']['scor'],
                teamwork=parsed['data']['twsc'],
                combat=parsed['data']['cmsc'],
                commander=parsed['data']['cdsc'],
                best_round=parsed['data']['bbrs'],
                per_minute=parsed['data']['ospm']
            ),
            time=PlayerinfoTimes(
                total=parsed['data']['time'],
                commander=parsed['data']['tcdr'],
                squad_leader=parsed['data']['tsql'],
                squad_member=parsed['data']['tsqm'],
                lone_wolf=parsed['data']['tlwf']
            ),
            rounds=PlayerinfoRounds(
                conquest=parsed['data']['mode0'],
                supply_lines=parsed['data']['mode1'],
                coop=parsed['data']['mode2'],
                wins=parsed['data']['wins'],
                losses=parsed['data']['loss']
            ),
            kills=PlayerinfoKills(
                total=parsed['data']['kill'],
                streak=parsed['data']['bksk'],
                per_minute=parsed['data']['klpm'],
                per_round=parsed['data']['klpr']
            ),
            deaths=PlayerinfoDeaths(
                total=parsed['data']['deth'],
                suicides=parsed['data']['suic'],
                streak=parsed['data']['wdsk'],
                per_minute=parsed['data']['dtpm'],
                per_round=parsed['data']['dtpr']
            ),
            teamwork=PlayerinfoTeamwork(
                flag_captures=parsed['data']['cpcp'],
                flag_assists=parsed['data']['cacp'],
                flag_defends=parsed['data']['dfcp'],
                kill_assists=parsed['data']['kila'],
                target_assists=parsed['data']['tgte'],
                heals=parsed['data']['heal'],
                revives=parsed['data']['rviv'],
                resupplies=parsed['data']['rsup'],
                repairs=parsed['data']['rpar'],
                driver_assists=parsed['data']['dkas'],
                driver_specials=parsed['data']['dsab']
            ),
            tactical=PlayerinfoTactical(
                teargas_flashbang_deploys=parsed['data']['de-6'],
                grappling_hook_deploys=parsed['data']['de-7'],
                zipline_deploys=parsed['data']['de-8']
            ),
            favorite=PlayerinfoFavorites(
                kit=parsed['data']['fkit'],
                weapon=parsed['data']['fwea'],
                vehicle=parsed['data']['fveh'],
                map=parsed['data']['fmap']
            ),
            weapons=[
                PlayerinfoWeapon(
                    id=w['id'],
                    time=w['tm'],
                    kills=w['kl'],
                    deaths=w['dt'],
                    accuracy=w['ac'],
                    kd=w['kd']
                ) for w in group_stats_by_item(parsed['data'], 'w', ['tm', 'kl', 'dt', 'ac', 'kd'])
            ],
            vehicles=[
                PlayerinfoVehicle(
                    id=v['id'],
                    time=v['tm'],
                    kills=v['kl'],
                    deaths=v['dt'],
                    kd=v['kd'],
                    road_kills=v['kr']
                ) for v in group_stats_by_item(parsed['data'], 'v', ['tm', 'kl', 'dt', 'kd', 'kr'])
            ],
            armies=[
                PlayerinfoArmy(
                    id=a['id'],
                    time=a['tm'],
                    wins=a['wn'],
                    losses=a['lo'],
                    best_round_score=a['br']
                ) for a in group_stats_by_item(parsed['data'], 'a', ['tm', 'wn', 'lo', 'br'])
            ],
            kits=[
                PlayerinfoKit(
                    id=k['id'],
                    time=k['tm'],
                    kills=k['kl'],
                    deaths=k['dt'],
                    kd=k['kd']
                ) for k in group_stats_by_item(parsed['data'], 'k', ['tm', 'kl', 'dt', 'kd'])
            ],
            relations=PlayerinfoRelations(
                top_rival=PlayerinfoRelation(
                    pid=parsed['data']['topr'],
                    nick=parsed['data']['vmns'],
                    rank=parsed['data']['vmrs'],
                    kills=parsed['data']['vmks']
                ),
                top_victim=PlayerinfoRelation(
                    pid=parsed['data']['tvcr'],
                    nick=parsed['data']['mvns'],
                    rank=parsed['data']['mvrs'],
                    kills=parsed['data']['mvks']
                )
            )
        )


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

    @staticmethod
    def from_aspx_response(parsed: dict) -> 'PlayerinfoMapStats':
        return PlayerinfoMapStats(
                pid=parsed['data']['pid'],
                nick=parsed['data']['nick'],
                maps=[
                    PlayerinfoMap(
                        id=m['id'],
                        time=m['tm'],
                        wins=m['wn'],
                        losses=m['ls']
                    ) for m in group_stats_by_item(parsed['data'], 'm', ['tm', 'wn', 'ls'])
                ]
            )


@dataclass
class PlayerinfoResponse:
    asof: int
    data: Union[PlayerinfoGeneralStats, PlayerinfoMapStats]

    def __iter__(self):
        yield 'asof', self.asof
        yield 'data', dict(self.data)


@dataclass
class RankinfoData:
    rank: int
    promoted: bool
    demoted: bool

    def __iter__(self):
        yield 'rank', self.rank
        yield 'promoted', self.promoted
        yield 'demoted', self.demoted


@dataclass
class RankinfoResponse:
    data: RankinfoData

    def __iter__(self):
        yield 'data', dict(self.data)

    @staticmethod
    def from_aspx_response(parsed: dict) -> 'RankinfoResponse':
        return RankinfoResponse(
            data=RankinfoData(
                rank=parsed['data']['rank'],
                promoted=parsed['data']['chng'],
                demoted=parsed['data']['decr']
            )
        )
