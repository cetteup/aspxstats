from dataclasses import dataclass
from typing import List
from unittest import TestCase

from aspxstats import InvalidParameterError
from aspxstats.bf2 import AspxClient, StatsProvider
from aspxstats.types import ProviderConfig


class AspxClientTest(TestCase):
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
                name='false for non-dict in  entries',
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
            valid = AspxClient.is_valid_getleaderboard_score_response_data(t.parsed)

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
