from dataclasses import dataclass
from typing import List
from unittest import TestCase

from aspxstats.bf2 import Bf2AspxClient, Bf2StatsProvider
from aspxstats.common import ProviderConfig
from aspxstats.exceptions import InvalidParameterError


class Bf2AspxClientTest(TestCase):
    def test_is_valid_searchforplayers_response_data(self):
        @dataclass
        class TestCase:
            name: str
            parsed: dict
            wantIsValid: bool

        # GIVEN
        tests: List[TestCase] = [
            TestCase(
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
            TestCase(
                name='true for valid searchforplayers data without any results',
                parsed={
                    'asof': '1663447766',
                    'results': []
                },
                wantIsValid=True
            ),
            TestCase(
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
            TestCase(
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
            TestCase(
                name='false for results missing',
                parsed={
                    'asof': '1663447766'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for non-list results',
                parsed={
                    'asof': '1663447766',
                    'results': 'not-a-dict'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for invalid search result',
                parsed={
                    'asof': '1663447766',
                    'results': [
                        {
                            'n': 1,
                            'pid': '45377286',
                            'nick': 'mister249',
                            'score': '6458'
                        },
                    ]
                },
                wantIsValid=False
            ),
            TestCase(
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
            valid = Bf2AspxClient.is_valid_searchforplayers_response_data(t.parsed)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')

    def test_is_valid_searchforplayers_result_data(self):
        @dataclass
        class TestCase:
            name: str
            result: dict
            wantIsValid: bool

        # GIVEN
        tests: List[TestCase] = [
            TestCase(
                name='true for valid searchforplayers result',
                result={
                    'n': '1',
                    'pid': '45377286',
                    'nick': 'mister249',
                    'score': '6458'
                },
                wantIsValid=True
            ),
            TestCase(
                name='false for missing numeric string attribute',
                result={
                    'pid': '45377286',
                    'nick': 'mister249',
                    'score': '6458'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for non-string numeric string attribute',
                result={
                    'n': 1,
                    'pid': '45377286',
                    'nick': 'mister249',
                    'score': '6458'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for non-numeric string numeric string attribute',
                result={
                    'n': 'not-numeric',
                    'pid': '45377286',
                    'nick': 'mister249',
                    'score': '6458'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for missing nick',
                result={
                    'n': '1',
                    'pid': '45377286',
                    'score': '6458'
                },
                wantIsValid=False
            ),
            TestCase(
                name='false for non-string nick',
                result={
                    'n': '1',
                    'pid': '45377286',
                    'nick': 123456,
                    'score': '6458'
                },
                wantIsValid=False
            )
        ]

        for t in tests:
            # WHEN
            valid = Bf2AspxClient.is_valid_searchforplayers_result_data(t.result)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')

    def test_get_provider_config(self):
        # GIVEN
        provider = Bf2StatsProvider.BF2HUB

        # WHEN
        config = Bf2AspxClient.get_provider_config(provider)

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
            Bf2AspxClient.get_provider_config,
            provider
        )
