from typing import Dict, Union

from aspxstats.validation import AttributeSchema

SEARCHFORPLAYERS_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'asof': AttributeSchema(type=str, is_numeric=True),
    'results': AttributeSchema(type=list, children={
        'n': AttributeSchema(type=str, is_numeric=True),
        'pid': AttributeSchema(type=str, is_numeric=True),
        'nick': AttributeSchema(type=str),
        'score': AttributeSchema(type=str, is_numeric=True)
    })
}

GETLEADERBOARD_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'size': AttributeSchema(type=str, is_numeric=True),
    'asof': AttributeSchema(type=str, is_numeric=True),
    'entries': AttributeSchema(type=list, children={
        'n': AttributeSchema(type=str, is_numeric=True),
        'pid': AttributeSchema(type=str, is_numeric=True),
        'nick': AttributeSchema(type=str),
        'playerrank': AttributeSchema(type=str, is_numeric=True),
        'countrycode': AttributeSchema(type=str)
    })
}

GETPLAYERINFO_GENERAL_STATS_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'asof': AttributeSchema(type=str, is_numeric=True),
    'player': {
        'pid': AttributeSchema(type=str, is_numeric=True),
        'nick': AttributeSchema(type=str),
        'scor': AttributeSchema(type=str, is_numeric=True),
        'jond': AttributeSchema(type=str, is_numeric=True),
        'wins': AttributeSchema(type=str, is_numeric=True),
        'loss': AttributeSchema(type=str, is_numeric=True),
        'mode0': AttributeSchema(type=str, is_numeric=True),
        'mode1': AttributeSchema(type=str, is_numeric=True),
        'mode2': AttributeSchema(type=str, is_numeric=True),
        'time': AttributeSchema(type=str, is_numeric=True),
        'smoc': AttributeSchema(type=str, is_numeric=True),
        'cmsc': AttributeSchema(type=str, is_numeric=True),
        'osaa': AttributeSchema(type=str, is_floaty=True),
        'kill': AttributeSchema(type=str, is_numeric=True),
        'kila': AttributeSchema(type=str, is_numeric=True),
        'deth': AttributeSchema(type=str, is_numeric=True),
        'suic': AttributeSchema(type=str, is_numeric=True),
        'bksk': AttributeSchema(type=str, is_numeric=True),
        'wdsk': AttributeSchema(type=str, is_numeric=True),
        'tvcr': AttributeSchema(type=str, is_numeric=True),
        'topr': AttributeSchema(type=str, is_numeric=True),
        'klpm': AttributeSchema(type=str, is_floaty=True),
        'dtpm': AttributeSchema(type=str, is_floaty=True),
        'ospm': AttributeSchema(type=str, is_floaty=True),
        'klpr': AttributeSchema(type=str, is_floaty=True),
        'dtpr': AttributeSchema(type=str, is_floaty=True),
        'twsc': AttributeSchema(type=str, is_numeric=True),
        'cpcp': AttributeSchema(type=str, is_numeric=True),
        'cacp': AttributeSchema(type=str, is_numeric=True),
        'dfcp': AttributeSchema(type=str, is_numeric=True),
        'heal': AttributeSchema(type=str, is_numeric=True),
        'rviv': AttributeSchema(type=str, is_numeric=True),
        'rsup': AttributeSchema(type=str, is_numeric=True),
        'rpar': AttributeSchema(type=str, is_numeric=True),
        'tgte': AttributeSchema(type=str, is_numeric=True),
        'dkas': AttributeSchema(type=str, is_numeric=True),
        'dsab': AttributeSchema(type=str, is_numeric=True),
        'cdsc': AttributeSchema(type=str, is_numeric=True),
        'rank': AttributeSchema(type=str, is_numeric=True),
        'kick': AttributeSchema(type=str, is_numeric=True),
        'bbrs': AttributeSchema(type=str, is_numeric=True),
        'tcdr': AttributeSchema(type=str, is_numeric=True),
        'ban': AttributeSchema(type=str, is_numeric=True),
        'lbtl': AttributeSchema(type=str, is_numeric=True),
        'vrk': AttributeSchema(type=str, is_numeric=True),
        'tsql': AttributeSchema(type=str, is_numeric=True),
        'tsqm': AttributeSchema(type=str, is_numeric=True),
        'tlwf': AttributeSchema(type=str, is_numeric=True),
        'mvks': AttributeSchema(type=str, is_numeric=True),
        'vmks': AttributeSchema(type=str, is_numeric=True),
        'mvns': AttributeSchema(type=str),
        'mvrs': AttributeSchema(type=str, is_numeric=True),
        'vmns': AttributeSchema(type=str),
        'vmrs': AttributeSchema(type=str, is_numeric=True),
        'fkit': AttributeSchema(type=str, is_numeric=True),
        'fmap': AttributeSchema(type=str, is_numeric=True),
        'fveh': AttributeSchema(type=str, is_numeric=True),
        'fwea': AttributeSchema(type=str, is_numeric=True),
        'tnv': AttributeSchema(type=str, is_numeric=True),
        'tgm': AttributeSchema(type=str, is_numeric=True),
        'wtm-0': AttributeSchema(type=str, is_numeric=True),
        'wtm-1': AttributeSchema(type=str, is_numeric=True),
        'wtm-2': AttributeSchema(type=str, is_numeric=True),
        'wtm-3': AttributeSchema(type=str, is_numeric=True),
        'wtm-4': AttributeSchema(type=str, is_numeric=True),
        'wtm-5': AttributeSchema(type=str, is_numeric=True),
        'wtm-6': AttributeSchema(type=str, is_numeric=True),
        'wtm-7': AttributeSchema(type=str, is_numeric=True),
        'wtm-8': AttributeSchema(type=str, is_numeric=True),
        'wtm-9': AttributeSchema(type=str, is_numeric=True),
        'wtm-10': AttributeSchema(type=str, is_numeric=True),
        'wtm-11': AttributeSchema(type=str, is_numeric=True),
        'wtm-12': AttributeSchema(type=str, is_numeric=True),
        'wtm-13': AttributeSchema(type=str, is_numeric=True),
        'wkl-0': AttributeSchema(type=str, is_numeric=True),
        'wkl-1': AttributeSchema(type=str, is_numeric=True),
        'wkl-2': AttributeSchema(type=str, is_numeric=True),
        'wkl-3': AttributeSchema(type=str, is_numeric=True),
        'wkl-4': AttributeSchema(type=str, is_numeric=True),
        'wkl-5': AttributeSchema(type=str, is_numeric=True),
        'wkl-6': AttributeSchema(type=str, is_numeric=True),
        'wkl-7': AttributeSchema(type=str, is_numeric=True),
        'wkl-8': AttributeSchema(type=str, is_numeric=True),
        'wkl-9': AttributeSchema(type=str, is_numeric=True),
        'wkl-10': AttributeSchema(type=str, is_numeric=True),
        'wkl-11': AttributeSchema(type=str, is_numeric=True),
        'wkl-12': AttributeSchema(type=str, is_numeric=True),
        'wkl-13': AttributeSchema(type=str, is_numeric=True),
        'wdt-0': AttributeSchema(type=str, is_numeric=True),
        'wdt-1': AttributeSchema(type=str, is_numeric=True),
        'wdt-2': AttributeSchema(type=str, is_numeric=True),
        'wdt-3': AttributeSchema(type=str, is_numeric=True),
        'wdt-4': AttributeSchema(type=str, is_numeric=True),
        'wdt-5': AttributeSchema(type=str, is_numeric=True),
        'wdt-6': AttributeSchema(type=str, is_numeric=True),
        'wdt-7': AttributeSchema(type=str, is_numeric=True),
        'wdt-8': AttributeSchema(type=str, is_numeric=True),
        'wdt-9': AttributeSchema(type=str, is_numeric=True),
        'wdt-10': AttributeSchema(type=str, is_numeric=True),
        'wdt-11': AttributeSchema(type=str, is_numeric=True),
        'wdt-12': AttributeSchema(type=str, is_numeric=True),
        'wdt-13': AttributeSchema(type=str, is_numeric=True),
        'wac-0': AttributeSchema(type=str, is_floaty=True),
        'wac-1': AttributeSchema(type=str, is_floaty=True),
        'wac-2': AttributeSchema(type=str, is_floaty=True),
        'wac-3': AttributeSchema(type=str, is_floaty=True),
        'wac-4': AttributeSchema(type=str, is_floaty=True),
        'wac-5': AttributeSchema(type=str, is_floaty=True),
        'wac-6': AttributeSchema(type=str, is_floaty=True),
        'wac-7': AttributeSchema(type=str, is_floaty=True),
        'wac-8': AttributeSchema(type=str, is_floaty=True),
        'wac-9': AttributeSchema(type=str, is_floaty=True),
        'wac-10': AttributeSchema(type=str, is_floaty=True),
        'wac-11': AttributeSchema(type=str, is_floaty=True),
        'wac-12': AttributeSchema(type=str, is_floaty=True),
        'wac-13': AttributeSchema(type=str, is_floaty=True),
        'wkd-0': AttributeSchema(type=str),
        'wkd-1': AttributeSchema(type=str),
        'wkd-2': AttributeSchema(type=str),
        'wkd-3': AttributeSchema(type=str),
        'wkd-4': AttributeSchema(type=str),
        'wkd-5': AttributeSchema(type=str),
        'wkd-6': AttributeSchema(type=str),
        'wkd-7': AttributeSchema(type=str),
        'wkd-8': AttributeSchema(type=str),
        'wkd-9': AttributeSchema(type=str),
        'wkd-10': AttributeSchema(type=str),
        'wkd-11': AttributeSchema(type=str),
        'wkd-12': AttributeSchema(type=str),
        'wkd-13': AttributeSchema(type=str),
        'vtm-0': AttributeSchema(type=str, is_numeric=True),
        'vtm-1': AttributeSchema(type=str, is_numeric=True),
        'vtm-2': AttributeSchema(type=str, is_numeric=True),
        'vtm-3': AttributeSchema(type=str, is_numeric=True),
        'vtm-4': AttributeSchema(type=str, is_numeric=True),
        'vtm-5': AttributeSchema(type=str, is_numeric=True),
        'vtm-6': AttributeSchema(type=str, is_numeric=True),
        'vkl-0': AttributeSchema(type=str, is_numeric=True),
        'vkl-1': AttributeSchema(type=str, is_numeric=True),
        'vkl-2': AttributeSchema(type=str, is_numeric=True),
        'vkl-3': AttributeSchema(type=str, is_numeric=True),
        'vkl-4': AttributeSchema(type=str, is_numeric=True),
        'vkl-5': AttributeSchema(type=str, is_numeric=True),
        'vkl-6': AttributeSchema(type=str, is_numeric=True),
        'vdt-0': AttributeSchema(type=str, is_numeric=True),
        'vdt-1': AttributeSchema(type=str, is_numeric=True),
        'vdt-2': AttributeSchema(type=str, is_numeric=True),
        'vdt-3': AttributeSchema(type=str, is_numeric=True),
        'vdt-4': AttributeSchema(type=str, is_numeric=True),
        'vdt-5': AttributeSchema(type=str, is_numeric=True),
        'vdt-6': AttributeSchema(type=str, is_numeric=True),
        'vkd-0': AttributeSchema(type=str),
        'vkd-1': AttributeSchema(type=str),
        'vkd-2': AttributeSchema(type=str),
        'vkd-3': AttributeSchema(type=str),
        'vkd-4': AttributeSchema(type=str),
        'vkd-5': AttributeSchema(type=str),
        'vkd-6': AttributeSchema(type=str),
        'vkr-0': AttributeSchema(type=str, is_numeric=True),
        'vkr-1': AttributeSchema(type=str, is_numeric=True),
        'vkr-2': AttributeSchema(type=str, is_numeric=True),
        'vkr-3': AttributeSchema(type=str, is_numeric=True),
        'vkr-4': AttributeSchema(type=str, is_numeric=True),
        'vkr-5': AttributeSchema(type=str, is_numeric=True),
        'vkr-6': AttributeSchema(type=str, is_numeric=True),
        'atm-0': AttributeSchema(type=str, is_numeric=True),
        'atm-1': AttributeSchema(type=str, is_numeric=True),
        'atm-2': AttributeSchema(type=str, is_numeric=True),
        'atm-3': AttributeSchema(type=str, is_numeric=True),
        'atm-4': AttributeSchema(type=str, is_numeric=True),
        'atm-5': AttributeSchema(type=str, is_numeric=True),
        'atm-6': AttributeSchema(type=str, is_numeric=True),
        'atm-7': AttributeSchema(type=str, is_numeric=True),
        'atm-8': AttributeSchema(type=str, is_numeric=True),
        'atm-9': AttributeSchema(type=str, is_numeric=True),
        'awn-0': AttributeSchema(type=str, is_numeric=True),
        'awn-1': AttributeSchema(type=str, is_numeric=True),
        'awn-2': AttributeSchema(type=str, is_numeric=True),
        'awn-3': AttributeSchema(type=str, is_numeric=True),
        'awn-4': AttributeSchema(type=str, is_numeric=True),
        'awn-5': AttributeSchema(type=str, is_numeric=True),
        'awn-6': AttributeSchema(type=str, is_numeric=True),
        'awn-7': AttributeSchema(type=str, is_numeric=True),
        'awn-8': AttributeSchema(type=str, is_numeric=True),
        'awn-9': AttributeSchema(type=str, is_numeric=True),
        'alo-0': AttributeSchema(type=str, is_numeric=True),
        'alo-1': AttributeSchema(type=str, is_numeric=True),
        'alo-2': AttributeSchema(type=str, is_numeric=True),
        'alo-3': AttributeSchema(type=str, is_numeric=True),
        'alo-4': AttributeSchema(type=str, is_numeric=True),
        'alo-5': AttributeSchema(type=str, is_numeric=True),
        'alo-6': AttributeSchema(type=str, is_numeric=True),
        'alo-7': AttributeSchema(type=str, is_numeric=True),
        'alo-8': AttributeSchema(type=str, is_numeric=True),
        'alo-9': AttributeSchema(type=str, is_numeric=True),
        'abr-0': AttributeSchema(type=str, is_numeric=True),
        'abr-1': AttributeSchema(type=str, is_numeric=True),
        'abr-2': AttributeSchema(type=str, is_numeric=True),
        'abr-3': AttributeSchema(type=str, is_numeric=True),
        'abr-4': AttributeSchema(type=str, is_numeric=True),
        'abr-5': AttributeSchema(type=str, is_numeric=True),
        'abr-6': AttributeSchema(type=str, is_numeric=True),
        'abr-7': AttributeSchema(type=str, is_numeric=True),
        'abr-8': AttributeSchema(type=str, is_numeric=True),
        'abr-9': AttributeSchema(type=str, is_numeric=True),
        'ktm-0': AttributeSchema(type=str, is_numeric=True),
        'ktm-1': AttributeSchema(type=str, is_numeric=True),
        'ktm-2': AttributeSchema(type=str, is_numeric=True),
        'ktm-3': AttributeSchema(type=str, is_numeric=True),
        'ktm-4': AttributeSchema(type=str, is_numeric=True),
        'ktm-5': AttributeSchema(type=str, is_numeric=True),
        'ktm-6': AttributeSchema(type=str, is_numeric=True),
        'kkl-0': AttributeSchema(type=str, is_numeric=True),
        'kkl-1': AttributeSchema(type=str, is_numeric=True),
        'kkl-2': AttributeSchema(type=str, is_numeric=True),
        'kkl-3': AttributeSchema(type=str, is_numeric=True),
        'kkl-4': AttributeSchema(type=str, is_numeric=True),
        'kkl-5': AttributeSchema(type=str, is_numeric=True),
        'kkl-6': AttributeSchema(type=str, is_numeric=True),
        'kdt-0': AttributeSchema(type=str, is_numeric=True),
        'kdt-1': AttributeSchema(type=str, is_numeric=True),
        'kdt-2': AttributeSchema(type=str, is_numeric=True),
        'kdt-3': AttributeSchema(type=str, is_numeric=True),
        'kdt-4': AttributeSchema(type=str, is_numeric=True),
        'kdt-5': AttributeSchema(type=str, is_numeric=True),
        'kdt-6': AttributeSchema(type=str, is_numeric=True),
        'kkd-0': AttributeSchema(type=str),
        'kkd-1': AttributeSchema(type=str),
        'kkd-2': AttributeSchema(type=str),
        'kkd-3': AttributeSchema(type=str),
        'kkd-4': AttributeSchema(type=str),
        'kkd-5': AttributeSchema(type=str),
        'kkd-6': AttributeSchema(type=str),
        'de-6': AttributeSchema(type=str, is_numeric=True),
        'de-7': AttributeSchema(type=str, is_numeric=True),
        'de-8': AttributeSchema(type=str, is_numeric=True),

    }
}

GETPLAYERINFO_MAP_STATS_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'asof': AttributeSchema(type=str, is_numeric=True),
    'player': {
        'pid': AttributeSchema(type=str, is_numeric=True),
        'nick': AttributeSchema(type=str),
        'mtm-0': AttributeSchema(type=str, is_numeric=True),
        'mtm-1': AttributeSchema(type=str, is_numeric=True),
        'mtm-2': AttributeSchema(type=str, is_numeric=True),
        'mtm-3': AttributeSchema(type=str, is_numeric=True),
        'mtm-4': AttributeSchema(type=str, is_numeric=True),
        'mtm-5': AttributeSchema(type=str, is_numeric=True),
        'mtm-6': AttributeSchema(type=str, is_numeric=True),
        'mtm-10': AttributeSchema(type=str, is_numeric=True),
        'mtm-11': AttributeSchema(type=str, is_numeric=True),
        'mtm-12': AttributeSchema(type=str, is_numeric=True),
        'mtm-100': AttributeSchema(type=str, is_numeric=True),
        'mtm-101': AttributeSchema(type=str, is_numeric=True),
        'mtm-102': AttributeSchema(type=str, is_numeric=True),
        'mtm-103': AttributeSchema(type=str, is_numeric=True),
        'mtm-104': AttributeSchema(type=str, is_numeric=True),
        'mtm-105': AttributeSchema(type=str, is_numeric=True),
        'mtm-110': AttributeSchema(type=str, is_numeric=True),
        'mtm-200': AttributeSchema(type=str, is_numeric=True),
        'mtm-201': AttributeSchema(type=str, is_numeric=True),
        'mtm-202': AttributeSchema(type=str, is_numeric=True),
        'mtm-300': AttributeSchema(type=str, is_numeric=True),
        'mtm-301': AttributeSchema(type=str, is_numeric=True),
        'mtm-302': AttributeSchema(type=str, is_numeric=True),
        'mtm-303': AttributeSchema(type=str, is_numeric=True),
        'mtm-304': AttributeSchema(type=str, is_numeric=True),
        'mtm-305': AttributeSchema(type=str, is_numeric=True),
        'mtm-306': AttributeSchema(type=str, is_numeric=True),
        'mtm-307': AttributeSchema(type=str, is_numeric=True),
        'mtm-601': AttributeSchema(type=str, is_numeric=True),
        'mwn-0': AttributeSchema(type=str, is_numeric=True),
        'mwn-1': AttributeSchema(type=str, is_numeric=True),
        'mwn-2': AttributeSchema(type=str, is_numeric=True),
        'mwn-3': AttributeSchema(type=str, is_numeric=True),
        'mwn-4': AttributeSchema(type=str, is_numeric=True),
        'mwn-5': AttributeSchema(type=str, is_numeric=True),
        'mwn-6': AttributeSchema(type=str, is_numeric=True),
        'mwn-10': AttributeSchema(type=str, is_numeric=True),
        'mwn-11': AttributeSchema(type=str, is_numeric=True),
        'mwn-12': AttributeSchema(type=str, is_numeric=True),
        'mwn-100': AttributeSchema(type=str, is_numeric=True),
        'mwn-101': AttributeSchema(type=str, is_numeric=True),
        'mwn-102': AttributeSchema(type=str, is_numeric=True),
        'mwn-103': AttributeSchema(type=str, is_numeric=True),
        'mwn-104': AttributeSchema(type=str, is_numeric=True),
        'mwn-105': AttributeSchema(type=str, is_numeric=True),
        'mwn-110': AttributeSchema(type=str, is_numeric=True),
        'mwn-200': AttributeSchema(type=str, is_numeric=True),
        'mwn-201': AttributeSchema(type=str, is_numeric=True),
        'mwn-202': AttributeSchema(type=str, is_numeric=True),
        'mwn-300': AttributeSchema(type=str, is_numeric=True),
        'mwn-301': AttributeSchema(type=str, is_numeric=True),
        'mwn-302': AttributeSchema(type=str, is_numeric=True),
        'mwn-303': AttributeSchema(type=str, is_numeric=True),
        'mwn-304': AttributeSchema(type=str, is_numeric=True),
        'mwn-305': AttributeSchema(type=str, is_numeric=True),
        'mwn-306': AttributeSchema(type=str, is_numeric=True),
        'mwn-307': AttributeSchema(type=str, is_numeric=True),
        'mwn-601': AttributeSchema(type=str, is_numeric=True),
        'mls-0': AttributeSchema(type=str, is_numeric=True),
        'mls-1': AttributeSchema(type=str, is_numeric=True),
        'mls-2': AttributeSchema(type=str, is_numeric=True),
        'mls-3': AttributeSchema(type=str, is_numeric=True),
        'mls-4': AttributeSchema(type=str, is_numeric=True),
        'mls-5': AttributeSchema(type=str, is_numeric=True),
        'mls-6': AttributeSchema(type=str, is_numeric=True),
        'mls-10': AttributeSchema(type=str, is_numeric=True),
        'mls-11': AttributeSchema(type=str, is_numeric=True),
        'mls-12': AttributeSchema(type=str, is_numeric=True),
        'mls-100': AttributeSchema(type=str, is_numeric=True),
        'mls-101': AttributeSchema(type=str, is_numeric=True),
        'mls-102': AttributeSchema(type=str, is_numeric=True),
        'mls-103': AttributeSchema(type=str, is_numeric=True),
        'mls-104': AttributeSchema(type=str, is_numeric=True),
        'mls-105': AttributeSchema(type=str, is_numeric=True),
        'mls-110': AttributeSchema(type=str, is_numeric=True),
        'mls-200': AttributeSchema(type=str, is_numeric=True),
        'mls-201': AttributeSchema(type=str, is_numeric=True),
        'mls-202': AttributeSchema(type=str, is_numeric=True),
        'mls-300': AttributeSchema(type=str, is_numeric=True),
        'mls-301': AttributeSchema(type=str, is_numeric=True),
        'mls-302': AttributeSchema(type=str, is_numeric=True),
        'mls-303': AttributeSchema(type=str, is_numeric=True),
        'mls-304': AttributeSchema(type=str, is_numeric=True),
        'mls-305': AttributeSchema(type=str, is_numeric=True),
        'mls-306': AttributeSchema(type=str, is_numeric=True),
        'mls-307': AttributeSchema(type=str, is_numeric=True),
        'mls-601': AttributeSchema(type=str, is_numeric=True)
    }
}
