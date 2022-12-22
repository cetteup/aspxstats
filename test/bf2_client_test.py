import unittest
from dataclasses import dataclass
from typing import List

from aspxstats import InvalidParameterError
from aspxstats.bf2 import AspxClient, StatsProvider
from aspxstats.bf2.types import PlayerinfoKeySet
from aspxstats.types import ProviderConfig


class AspxClientTest(unittest.TestCase):
    def test_is_valid_searchforplayers_response_data(self):
        @dataclass
        class SearchforplayersTestCase:
            name: str
            parsed: dict
            wantIsValid: bool

        # GIVEN
        tests: List[SearchforplayersTestCase] = [
            SearchforplayersTestCase(
                name='true for valid searchforplayers data',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                        {
                            'n': '2',
                            'pid': '500362798',
                            'nick': 'mister2499',
                            'score': '86136'
                        }
                    ]
                },
                wantIsValid=True
            ),
            SearchforplayersTestCase(
                name='true for valid searchforplayers data without any results',
                parsed={
                    'asof': '1663447766',
                    'results': []
                },
                wantIsValid=True
            ),
            SearchforplayersTestCase(
                name='false for missing asof',
                parsed={
                    'results': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for non-string asof',
                parsed={
                    'asof': 1663447766,
                    'results': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for results missing',
                parsed={
                    'asof': '1663447766'
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for non-list results',
                parsed={
                    'asof': '1663447766',
                    'results': 'not-a-list'
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for non-dict in results',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        'not-a-dict'
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for search result containing non-numeric-string numeric-string attribute',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'n': 'abddef',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for search result containing non-string string attribute',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 123456,
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for search result missing an attribute',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            SearchforplayersTestCase(
                name='false for valid search result followed by invalid',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                        {
                            'n': '2',
                            'pid': '500362798',
                            'nick': 'mister2499',
                            'score': 86136
                        }
                    ]
                },
                wantIsValid=False
            ),
        ]

        for t in tests:
            # WHEN
            valid = AspxClient.is_valid_searchforplayers_response_data(t.parsed)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')

    def test_is_valid_getleaderboard_response_data(self):
        @dataclass
        class GetleaderboardTestCase:
            name: str
            parsed: dict
            wantIsValid: bool

        # GIVEN
        tests: List[GetleaderboardTestCase] = [
            GetleaderboardTestCase(
                name='true for valid getleaderboard data',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'countrycode': 'DE'
                        },
                        {
                            'n': '2',
                            'pid': '500362798',
                            'nick': 'mister2499',
                            'playerrank': '6',
                            'countrycode': 'UA'
                        }
                    ]
                },
                wantIsValid=True
            ),
            GetleaderboardTestCase(
                name='true for valid getleaderboard data without any entries',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': []
                },
                wantIsValid=True
            ),
            GetleaderboardTestCase(
                name='false for missing size',
                parsed={
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for non-string size',
                parsed={
                    'size': 100000,
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for missing asof',
                parsed={
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for non-string asof',
                parsed={
                    'asof': 1663447766,
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for entries missing',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for non-list entries',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': 'not-a-list'
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for non-dict in entries',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        'not-a-dict'
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for search result containing non-numeric-string numeric-string attribute',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': 'abcdef',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for search result containing non-string string attribute',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 123456,
                            'playerrank': '13',
                            'country_code': 'DE'
                        }
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for search result missing an attribute',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        {
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        },
                    ]
                },
                wantIsValid=False
            ),
            GetleaderboardTestCase(
                name='false for valid search result followed by invalid',
                parsed={
                    'size': '100000',
                    'asof': '1663447766',
                    'entries': [
                        {
                            'n': '1',
                            'pid': '45377286',
                            'nick': 'mister249',
                            'playerrank': '13',
                            'country_code': 'DE'
                        },
                        {
                            'n': '2',
                            'pid': '500362798',
                            'nick': 'mister2499',
                            'playerrank': 8,
                            'country_code': 'UA'
                        }
                    ]
                },
                wantIsValid=False
            ),
        ]

        for t in tests:
            # WHEN
            valid = AspxClient.is_valid_getleaderboard_response_data(t.parsed)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')

    def test_is_valid_getplayerinfo_response_data_general_stats_player_attributes(self):
        # GIVEN
        parsed = {
            'asof': '1663620931',
            'data': {
                'pid': '500362798', 'nick': 'mister249', 'scor': '86469', 'jond': '1601656220', 'wins': '630',
                'loss': '575', 'mode0': '1206', 'mode1': '0', 'mode2': '0', 'time': '1319254', 'smoc': '0',
                'cmsc': '38689868', 'osaa': '28.402304270517', 'kill': '30103', 'kila': '4578', 'deth': '12303',
                'suic': '393', 'bksk': '49', 'wdsk': '13', 'tvcr': '338150598', 'topr': '500351628', 'klpm': '1.38',
                'dtpm': '0.56', 'ospm': '3.96', 'klpr': '50.42', 'dtpr': '20.61', 'twsc': '23537', 'cpcp': '2251',
                'cacp': '2726', 'dfcp': '822', 'heal': '1193', 'rviv': '4852', 'rsup': '1674', 'rpar': '139',
                'tgte': '41', 'dkas': '471', 'dsab': '41', 'cdsc': '3923', 'rank': '13', 'kick': '6', 'bbrs': '266',
                'tcdr': '107387', 'ban': '0', 'lbtl': '1663620928', 'vrk': '91402', 'tsql': '444505', 'tsqm': '714563',
                'tlwf': '52155', 'mvks': '22', 'vmks': '16', 'mvns': 'Volk[by]3', 'mvrs': '17',
                'vmns': 'Noooooooooooooooooob', 'vmrs': '6', 'fkit': '6', 'fmap': '4', 'fveh': '0', 'fwea': '4',
                'tnv': '0', 'tgm': '0', 'wtm-0': '212185', 'wtm-1': '3770', 'wtm-2': '44456', 'wtm-3': '94651',
                'wtm-4': '304953', 'wtm-5': '44238', 'wtm-6': '99454', 'wtm-7': '35822', 'wtm-8': '47201',
                'wtm-9': '17780', 'wtm-10': '13519', 'wtm-11': '5291', 'wtm-12': '14503', 'wtm-13': '166',
                'wkl-0': '7419', 'wkl-1': '38', 'wkl-2': '1163', 'wkl-3': '3585', 'wkl-4': '8880', 'wkl-5': '1859',
                'wkl-6': '914', 'wkl-7': '989', 'wkl-8': '1226', 'wkl-9': '348', 'wkl-10': '196', 'wkl-11': '243',
                'wkl-12': '880', 'wkl-13': '0', 'wdt-0': '2464', 'wdt-1': '27', 'wdt-2': '534', 'wdt-3': '1366',
                'wdt-4': '2492', 'wdt-5': '1044', 'wdt-6': '952', 'wdt-7': '576', 'wdt-8': '600', 'wdt-9': '241',
                'wdt-10': '288', 'wdt-11': '64', 'wdt-12': '131', 'wdt-13': '0', 'wac-0': '20.212175373033',
                'wac-1': '29.79274611399', 'wac-2': '25.621227011091', 'wac-3': '13.315454743968',
                'wac-4': '30.580768078092', 'wac-5': '22.05819474762', 'wac-6': '40.411582589692',
                'wac-7': '20.629418347572', 'wac-8': '9.5440084835631', 'wac-9': '9.6239485403266',
                'wac-10': '79.728533490705', 'wac-11': '24.695928080381', 'wac-12': '31.349325337331', 'wac-13': '0',
                'wkd-0': '7419:2464', 'wkd-1': '38:27', 'wkd-2': '1163:534', 'wkd-3': '3585:1366', 'wkd-4': '2220:623',
                'wkd-5': '1859:1044', 'wkd-6': '457:476', 'wkd-7': '989:576', 'wkd-8': '613:300', 'wkd-9': '348:241',
                'wkd-10': '49:72', 'wkd-11': '243:64', 'wkd-12': '880:131', 'wkd-13': '0', 'vtm-0': '53668',
                'vtm-1': '5366', 'vtm-2': '27820', 'vtm-3': '47261', 'vtm-4': '48384', 'vtm-5': '0', 'vtm-6': '6009',
                'vkl-0': '1058', 'vkl-1': '48', 'vkl-2': '348', 'vkl-3': '616', 'vkl-4': '487', 'vkl-5': '0',
                'vkl-6': '118', 'vdt-0': '229', 'vdt-1': '33', 'vdt-2': '106', 'vdt-3': '354', 'vdt-4': '231',
                'vdt-5': '0', 'vdt-6': '26', 'vkd-0': '1058:229', 'vkd-1': '16:11', 'vkd-2': '174:53',
                'vkd-3': '308:177', 'vkd-4': '487:231', 'vkd-5': '0', 'vkd-6': '59:13', 'vkr-0': '71', 'vkr-1': '10',
                'vkr-2': '22', 'vkr-3': '36', 'vkr-4': '36', 'vkr-5': '0', 'vkr-6': '2', 'atm-0': '675025',
                'atm-1': '533750', 'atm-2': '98271', 'atm-3': '3181', 'atm-4': '0', 'atm-5': '4459', 'atm-6': '703',
                'atm-7': '138', 'atm-8': '0', 'atm-9': '3646', 'awn-0': '284', 'awn-1': '280', 'awn-2': '63',
                'awn-3': '0', 'awn-4': '0', 'awn-5': '1', 'awn-6': '0', 'awn-7': '1', 'awn-8': '0', 'awn-9': '1',
                'alo-0': '296', 'alo-1': '203', 'alo-2': '70', 'alo-3': '1', 'alo-4': '0', 'alo-5': '1', 'alo-6': '1',
                'alo-7': '0', 'alo-8': '0', 'alo-9': '3', 'abr-0': '256', 'abr-1': '266', 'abr-2': '95', 'abr-3': '164',
                'abr-4': '0', 'abr-5': '140', 'abr-6': '12', 'abr-7': '0', 'abr-8': '0', 'abr-9': '87',
                'ktm-0': '229280', 'ktm-1': '64723', 'ktm-2': '131592', 'ktm-3': '254955', 'ktm-4': '60838',
                'ktm-5': '109804', 'ktm-6': '338127', 'kkl-0': '3914', 'kkl-1': '1754', 'kkl-2': '2358',
                'kkl-3': '7251', 'kkl-4': '1444', 'kkl-5': '3847', 'kkl-6': '10461', 'kdt-0': '2276', 'kdt-1': '720',
                'kdt-2': '901', 'kdt-3': '3039', 'kdt-4': '615', 'kdt-5': '1442', 'kdt-6': '3287', 'kkd-0': '1957:1138',
                'kkd-1': '877:360', 'kkd-2': '2358:901', 'kkd-3': '2417:1013', 'kkd-4': '1444:615',
                'kkd-5': '3847:1442', 'kkd-6': '10461:3287', 'de-6': '12', 'de-7': '13', 'de-8': '15'
            }
        }
        numeric_keys = [
            'scor', 'jond', 'wins', 'loss', 'mode0', 'mode1', 'mode2', 'time', 'cmsc', 'kill',
            'kila', 'deth', 'suic', 'bksk', 'wdsk', 'tvcr', 'topr', 'twsc', 'cpcp', 'cacp', 'dfcp', 'heal',
            'rviv', 'rsup', 'rpar', 'tgte', 'dkas', 'dsab', 'cdsc', 'rank', 'kick', 'bbrs', 'tcdr', 'ban',
            'lbtl', 'vrk', 'tsql', 'tsqm', 'tlwf', 'mvks', 'vmks', 'mvrs', 'vmrs', 'fkit', 'fmap', 'fveh',
            'fwea', 'tnv', 'tgm', 'wtm-0', 'wtm-1', 'wtm-2', 'wtm-3', 'wtm-4', 'wtm-5', 'wtm-6', 'wtm-7',
            'wtm-8', 'wtm-9', 'wtm-10', 'wtm-11', 'wtm-12', 'wtm-13', 'wkl-0', 'wkl-1', 'wkl-2', 'wkl-3',
            'wkl-4', 'wkl-5', 'wkl-6', 'wkl-7', 'wkl-8', 'wkl-9', 'wkl-10', 'wkl-11', 'wkl-12', 'wkl-13',
            'wdt-0', 'wdt-1', 'wdt-2', 'wdt-3', 'wdt-4', 'wdt-5', 'wdt-6', 'wdt-7', 'wdt-8', 'wdt-9',
            'wdt-10', 'wdt-11', 'wdt-12', 'wdt-13', 'vtm-0', 'vtm-1', 'vtm-2', 'vtm-3', 'vtm-4', 'vtm-5',
            'vtm-6', 'vkl-0', 'vkl-1', 'vkl-2', 'vkl-3', 'vkl-4', 'vkl-5', 'vkl-6', 'vdt-0', 'vdt-1',
            'vdt-2', 'vdt-3', 'vdt-4', 'vdt-5', 'vdt-6', 'vkr-0', 'vkr-1', 'vkr-2', 'vkr-3', 'vkr-4',
            'vkr-5', 'vkr-6', 'atm-0', 'atm-1', 'atm-2', 'atm-3', 'atm-4', 'atm-5', 'atm-6', 'atm-7',
            'atm-8', 'atm-9', 'awn-0', 'awn-1', 'awn-2', 'awn-3', 'awn-4', 'awn-5', 'awn-6', 'awn-7',
            'awn-8', 'awn-9', 'alo-0', 'alo-1', 'alo-2', 'alo-3', 'alo-4', 'alo-5', 'alo-6', 'alo-7',
            'alo-8', 'alo-9', 'abr-0', 'abr-1', 'abr-2', 'abr-3', 'abr-4', 'abr-5', 'abr-6', 'abr-7',
            'abr-8', 'abr-9', 'ktm-0', 'ktm-1', 'ktm-2', 'ktm-3', 'ktm-4', 'ktm-5', 'ktm-6', 'kkl-0',
            'kkl-1', 'kkl-2', 'kkl-3', 'kkl-4', 'kkl-5', 'kkl-6', 'kdt-0', 'kdt-1', 'kdt-2', 'kdt-3',
            'kdt-4', 'kdt-5', 'kdt-6', 'de-6', 'de-7', 'de-8'
        ]
        booly_keys = ['smoc']
        floaty_keys = [
            'osaa', 'klpm', 'dtpm', 'ospm', 'klpr', 'dtpr', 'wac-0', 'wac-1', 'wac-2', 'wac-3', 'wac-4', 'wac-5',
            'wac-6', 'wac-7', 'wac-8', 'wac-9', 'wac-10', 'wac-11', 'wac-12', 'wac-13'
        ]

        # WHEN
        valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed)

        # THEN
        self.assertTrue(valid)

        for key in parsed.keys():
            # Test with a copy
            parsed_copy = {
                'asof': parsed['asof'],
                'data': parsed['data'].copy()
            }

            # Attribute should be a string or dict => test with an int
            # GIVEN
            parsed_copy[key] = 123456
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" with non-string value failed')

            # Every attribute must be present => test without it
            # GIVEN
            del parsed_copy[key]
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" missing failed')

        for key in parsed['data'].keys():
            # Test with a copy
            parsed_copy = {
                'asof': parsed['asof'],
                'data': parsed['data'].copy()
            }

            # Every attribute should be a string => test with a non-string
            # GIVEN
            parsed_copy['data'][key] = 123456
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" with non-string value failed')

            # Every attribute must be present => test without it
            # GIVEN
            del parsed_copy['data'][key]
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" missing failed')

            if key in numeric_keys:
                # Attribute should be numeric => test with a non-numeric-string
                # GIVEN
                parsed_copy['data'][key] = 'not-a-numeric-string'
                # WHEN
                valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
                # THEN
                self.assertFalse(valid, f'"{key}" with non-numeric-string value failed')

            if key in booly_keys:
                # Attribute should be boolean-like numeric string => test with a non-booly-string
                # GIVEN
                parsed_copy['data'][key] = '2'
                # WHEN
                valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
                # THEN
                self.assertFalse(valid, f'"{key}" with non-booly-string value failed')

            if key in floaty_keys:
                # Attribute should be floaty => test with a non-floaty-string
                # GIVEN
                parsed_copy['data'][key] = 'not-a-floaty-string'
                # WHEN
                valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.GENERAL_STATS, parsed_copy)
                # THEN
                self.assertFalse(valid, f'"{key}" with non-floaty-string value failed')

    def test_is_valid_getplayerinfo_response_data_map_stats_player_attributes(self):
        # GIVEN
        parsed = {
            'asof': '1663620931',
            'data': {
                'pid': '500362798', 'nick': 'mister249', 'mtm-0': '101256', 'mtm-1': '21518', 'mtm-2': '13337',
                'mtm-3': '4156', 'mtm-4': '1276553', 'mtm-5': '17310', 'mtm-6': '63131', 'mtm-100': '48635',
                'mtm-101': '58559', 'mtm-102': '198609', 'mtm-103': '13690', 'mtm-104': '0', 'mtm-105': '5716',
                'mtm-601': '86401', 'mtm-300': '0', 'mtm-301': '5247', 'mtm-302': '0', 'mtm-303': '0', 'mtm-304': '0',
                'mtm-305': '3609', 'mtm-306': '2665', 'mtm-307': '3243', 'mtm-10': '850', 'mtm-11': '0',
                'mtm-110': '6544', 'mtm-200': '8018', 'mtm-201': '7616', 'mtm-202': '2701', 'mtm-12': '73338',
                'mwn-0': '31', 'mwn-1': '13', 'mwn-2': '3', 'mwn-3': '1', 'mwn-4': '395', 'mwn-5': '10', 'mwn-6': '24',
                'mwn-100': '11', 'mwn-101': '30', 'mwn-102': '45', 'mwn-103': '2', 'mwn-104': '0', 'mwn-105': '2',
                'mwn-601': '20', 'mwn-300': '0', 'mwn-301': '0', 'mwn-302': '0', 'mwn-303': '0', 'mwn-304': '0',
                'mwn-305': '1', 'mwn-306': '1', 'mwn-307': '0', 'mwn-10': '0', 'mwn-11': '0', 'mwn-110': '4',
                'mwn-200': '2', 'mwn-201': '5', 'mwn-202': '2', 'mwn-12': '22', 'mls-0': '27', 'mls-1': '9',
                'mls-2': '6', 'mls-3': '3', 'mls-4': '335', 'mls-5': '5', 'mls-6': '19', 'mls-100': '26',
                'mls-101': '18', 'mls-102': '37', 'mls-103': '9', 'mls-104': '0', 'mls-105': '3', 'mls-601': '27',
                'mls-300': '0', 'mls-301': '2', 'mls-302': '0', 'mls-303': '0', 'mls-304': '0', 'mls-305': '0',
                'mls-306': '0', 'mls-307': '1', 'mls-10': '1', 'mls-11': '0', 'mls-110': '2', 'mls-200': '3',
                'mls-201': '1', 'mls-202': '1', 'mls-12': '35'
            }
        }
        numeric_keys = [
            'mtm-0', 'mtm-1', 'mtm-2', 'mtm-3', 'mtm-4', 'mtm-5', 'mtm-6', 'mtm-10', 'mtm-11', 'mtm-12', 'mtm-100',
            'mtm-101', 'mtm-102', 'mtm-103', 'mtm-104', 'mtm-105', 'mtm-110', 'mtm-200', 'mtm-201', 'mtm-202',
            'mtm-300', 'mtm-301', 'mtm-302', 'mtm-303', 'mtm-304', 'mtm-305', 'mtm-306', 'mtm-307', 'mtm-601', 'mwn-0',
            'mwn-1', 'mwn-2', 'mwn-3', 'mwn-4', 'mwn-5', 'mwn-6', 'mwn-10', 'mwn-11', 'mwn-12', 'mwn-100', 'mwn-101',
            'mwn-102', 'mwn-103', 'mwn-104', 'mwn-105', 'mwn-110', 'mwn-200', 'mwn-201', 'mwn-202', 'mwn-300',
            'mwn-301', 'mwn-302', 'mwn-303', 'mwn-304', 'mwn-305', 'mwn-306', 'mwn-307', 'mwn-601', 'mls-0', 'mls-1',
            'mls-2', 'mls-3', 'mls-4', 'mls-5', 'mls-6', 'mls-10', 'mls-11', 'mls-12', 'mls-100', 'mls-101', 'mls-102',
            'mls-103', 'mls-104', 'mls-105', 'mls-110', 'mls-200', 'mls-201', 'mls-202', 'mls-300', 'mls-301',
            'mls-302', 'mls-303', 'mls-304', 'mls-305', 'mls-306', 'mls-307', 'mls-601'
        ]

        # WHEN
        valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed)

        # THEN
        self.assertTrue(valid)

        for key in parsed.keys():
            # Test with a copy
            parsed_copy = {
                'asof': parsed['asof'],
                'data': parsed['data'].copy()
            }

            # Attribute should be a string or dict => test with an int
            # GIVEN
            parsed_copy[key] = 123456
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" with non-string value failed')

            # Every attribute must be present => test without it
            # GIVEN
            del parsed_copy[key]
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" missing failed')

        for key in parsed['data'].keys():
            # Test with a copy
            parsed_copy = {
                'asof': parsed['asof'],
                'data': parsed['data'].copy()
            }

            # Every attribute should be a string => test with a non-string
            # GIVEN
            parsed_copy['data'][key] = 123456
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" with non-string value failed')

            # Every attribute must be present => test without it
            # GIVEN
            del parsed_copy['data'][key]
            # WHEN
            valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed_copy)
            # THEN
            self.assertFalse(valid, f'"{key}" missing failed')

            if key in numeric_keys:
                # Attribute should be numeric => test with a non-numeric-string
                # GIVEN
                parsed_copy['data'][key] = 'not-a-numeric-string'
                # WHEN
                valid = AspxClient.is_valid_getplayerinfo_response_data(PlayerinfoKeySet.MAP_STATS, parsed_copy)
                # THEN
                self.assertFalse(valid, f'"{key}" with non-numeric-string value failed')

    def test_fix_getplayerinfo_zero_values(self):
        @dataclass
        class FixGetplayerinfoTestCase:
            name: str
            parsed: dict
            expected: dict

        # GIVEN
        tests: List[FixGetplayerinfoTestCase] = [
            FixGetplayerinfoTestCase(
                name='replaces invalid zero values with "0"',
                parsed={
                    'data': {
                        'tvcr': '',
                        'topr': ' ',
                        'mvrs': 'NOT VAILABLE',
                        'vmrs': '0'
                    }
                },
                expected={
                    'data': {
                        'tvcr': '0',
                        'topr': '0',
                        'mvrs': '0',
                        'vmrs': '0'
                    }
                }
            ),
            FixGetplayerinfoTestCase(
                name='does not overwrite valid existing values',
                parsed={
                    'data': {
                        'tvcr': '1000',
                        'topr': '2000',
                        'mvrs': '3000',
                        'vmrs': '4000'
                    }
                },
                expected={
                    'data': {
                        'tvcr': '1000',
                        'topr': '2000',
                        'mvrs': '3000',
                        'vmrs': '4000'
                    }
                }
            ),
            FixGetplayerinfoTestCase(
                name='ignores any other keys',
                parsed={
                    'data': {
                        'tvcr': '',
                        'topr': ' ',
                        'mvrs': 'NOT VAILABLE',
                        'vmrs': '0',
                        'some-other-key': 'some-value'
                    },
                    'some-other-key': 'some-value'
                },
                expected={
                    'data': {
                        'tvcr': '0',
                        'topr': '0',
                        'mvrs': '0',
                        'vmrs': '0',
                        'some-other-key': 'some-value'
                    },
                    'some-other-key': 'some-value'
                }
            ),
            FixGetplayerinfoTestCase(
                name='does not add missing keys',
                parsed={
                    'data': {
                        'scor': '1000',
                        'tvcr': ''
                    }
                },
                expected={
                    'data': {
                        'scor': '1000',
                        'tvcr': '0'
                    }
                }
            ),
            FixGetplayerinfoTestCase(
                name='does nothing if player key is missing',
                parsed={
                    'some-other-key': 'some-value'
                },
                expected={
                    'some-other-key': 'some-value'
                }
            ),
            FixGetplayerinfoTestCase(
                name='does nothing if player key does not contain a dict',
                parsed={
                    'data': 'not-a-dict',
                    'some-other-key': 'some-value'
                },
                expected={
                    'data': 'not-a-dict',
                    'some-other-key': 'some-value'
                }
            ),
        ]

        for t in tests:
            # WHEN
            actual = AspxClient.fix_getplayerinfo_zero_values(t.parsed)

            # THEN
            self.assertDictEqual(t.expected, actual)

    def test_is_valid_getrankinfo_response_data(self):
        @dataclass
        class GetrankinfoTestCase:
            name: str
            parsed: dict
            wantIsValid: bool

        # GIVEN
        tests: List[GetrankinfoTestCase] = [
            GetrankinfoTestCase(
                name='true for valid getrankinfo data',
                parsed={
                    'data': {
                        'rank': '5',
                        'chng': '0',
                        'decr': '0'
                    }
                },
                wantIsValid=True
            ),
            GetrankinfoTestCase(
                name='false for missing data',
                parsed={
                    'some_key': {
                        'some_value': '5',
                    }
                },
                wantIsValid=False
            ),
            GetrankinfoTestCase(
                name='false for non-dict data',
                parsed={
                    'data': 'some-value'
                },
                wantIsValid=False
            ),
            GetrankinfoTestCase(
                name='false for data containing non-numeric-string numeric-string attribute',
                parsed={
                    'data': {
                        'rank': 'abcdef',
                        'chng': '0',
                        'decr': '0'
                    }
                },
                wantIsValid=False
            ),
            GetrankinfoTestCase(
                name='false for data containing non-booly-string booly-string attribute',
                parsed={
                    'data': {
                        'rank': '5',
                        'chng': '2',
                        'decr': '0'
                    }
                },
                wantIsValid=False
            ),
            GetrankinfoTestCase(
                name='false for missing data attribute',
                parsed={
                    'data': {
                        'chng': '0',
                        'decr': '0'
                    }
                },
                wantIsValid=False
            )
        ]

        for t in tests:
            # WHEN
            valid = AspxClient.is_valid_getrankinfo_response_data(t.parsed)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')

    def test_get_provider_config(self):
        # GIVEN
        provider = StatsProvider.BF2HUB

        # WHEN
        config = AspxClient.get_provider_config(provider)

        # THEN
        expected = ProviderConfig(
            base_uri='http://official.ranking.bf2hub.com/ASP/',
            default_headers={
                'Host': 'BF2web.gamespy.com',
                'User-Agent': 'GameSpyHTTP/1.0'
            }
        )
        self.assertEqual(expected.base_uri, config.base_uri)
        self.assertDictEqual(expected.default_headers, config.default_headers)

    def test_get_provider_config_error_for_unknown_provided(self):
        # GIVEN
        provider = 'not-a-supported-provider'

        # WHEN/THEN
        self.assertRaisesRegex(
            InvalidParameterError,
            '^No provider config for given provider.*$',
            AspxClient.get_provider_config,
            provider
        )


if __name__ == '__main__':
    unittest.main()
