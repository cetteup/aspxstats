from dataclasses import dataclass
from typing import List, Dict, Union
from unittest import TestCase

from aspxstats.bf2.utils import group_stats_by_item


class UtilsTest(TestCase):
    def test_group_stats_by_item(self):
        @dataclass
        class GroupStatsByItemTestCase:
            name: str
            data: Dict[str, Union[str, int, bool, float]]
            prefix: str
            keys: List[str]
            expected: List[Dict[str, Union[str, int, bool, float]]]

        tests: List[GroupStatsByItemTestCase] = [
            GroupStatsByItemTestCase(
                name='groups weapon stats',
                data={
                    'wtm-0': 123,
                    'wtm-10': 456,
                    'wkl-0': 321,
                    'wkl-10': 654,
                    'wdt-0': 789,
                    'wdt-10': 987,
                    'wac-0': 12.3,
                    'wac-10': 45.6,
                    'wkd-0': 65.4,
                    'wkd-10': 78.9
                },
                prefix='w',
                keys=['tm', 'kl', 'dt', 'ac', 'kd'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                        'kl': 321,
                        'dt': 789,
                        'ac': 12.3,
                        'kd': 65.4,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                        'kl': 654,
                        'dt': 987,
                        'ac': 45.6,
                        'kd': 78.9
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='groups vehicle stats',
                data={
                    'vtm-0': 123,
                    'vtm-10': 456,
                    'vkl-0': 321,
                    'vkl-10': 654,
                    'vdt-0': 789,
                    'vdt-10': 987,
                    'vkd-0': 65.4,
                    'vkd-10': 78.9,
                    'vkr-0': 123,
                    'vkr-10': 456
                },
                prefix='v',
                keys=['tm', 'kl', 'dt', 'kd', 'kr'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                        'kl': 321,
                        'dt': 789,
                        'kd': 65.4,
                        'kr': 123,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                        'kl': 654,
                        'dt': 987,
                        'kd': 78.9,
                        'kr': 456,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='groups army stats',
                data={
                    'atm-0': 123,
                    'atm-10': 456,
                    'awn-0': 321,
                    'awn-10': 654,
                    'alo-0': 789,
                    'alo-10': 987,
                    'abr-0': 123,
                    'abr-10': 456
                },
                prefix='a',
                keys=['tm', 'wn', 'lo', 'br'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                        'wn': 321,
                        'lo': 789,
                        'br': 123,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                        'wn': 654,
                        'lo': 987,
                        'br': 456,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='groups kit stats',
                data={
                    'ktm-0': 123,
                    'ktm-10': 456,
                    'kkl-0': 321,
                    'kkl-10': 654,
                    'kdt-0': 789,
                    'kdt-10': 987,
                    'kkd-0': 65.4,
                    'kkd-10': 78.9,
                },
                prefix='k',
                keys=['tm', 'kl', 'dt', 'kd'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                        'kl': 321,
                        'dt': 789,
                        'kd': 65.4,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                        'kl': 654,
                        'dt': 987,
                        'kd': 78.9,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='groups map stats',
                data={
                    'mtm-0': 123,
                    'mtm-10': 456,
                    'mwn-0': 321,
                    'mwn-10': 654,
                    'mls-0': 789,
                    'mls-10': 987,
                },
                prefix='m',
                keys=['tm', 'wn', 'ls'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                        'wn': 321,
                        'ls': 789,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                        'wn': 654,
                        'ls': 987,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='ignores keys not matching prefix',
                data={
                    'ptm-0': 123,
                    'ptm-10': 456,
                    'osaa': 12.3
                },
                prefix='p',
                keys=['tm'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='ignores keys not in key list',
                data={
                    'ptm-0': 123,
                    'ptm-10': 456,
                    'pin-0': 12.3
                },
                prefix='p',
                keys=['tm'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                    }
                ]
            ),
            GroupStatsByItemTestCase(
                name='ignores keys with non-numeric item id',
                data={
                    'ptm-0': 123,
                    'ptm-10': 456,
                    'ptm-a': 789
                },
                prefix='p',
                keys=['tm'],
                expected=[
                    {
                        'id': 0,
                        'tm': 123,
                    },
                    {
                        'id': 10,
                        'tm': 456,
                    }
                ]
            )
        ]

        for t in tests:
            # WHEN
            grouped = group_stats_by_item(t.data, t.prefix, t.keys)

            # THEN
            self.assertListEqual(t.expected, grouped)
