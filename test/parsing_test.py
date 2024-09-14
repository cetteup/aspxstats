from dataclasses import dataclass
from typing import Dict, Any, Union, List, Optional, Callable
from unittest import TestCase

from aspxstats.parsing import parse_dict_values
from aspxstats.schema import AttributeSchema
from aspxstats.types import CleanerType


class ParsingTest(TestCase):
    def test_parse(self):
        @dataclass
        class ParsingTestCase:
            name: str
            data: Dict[str, Any]
            schema: Dict[str, Union[AttributeSchema, dict]]
            expected: Dict[str, Any]
            cleaners: Optional[Dict[CleanerType, Callable[[str], str]]] = None

        # GIVEN
        tests: List[ParsingTestCase] = [
            ParsingTestCase(
                name='parses complex dict',
                data={
                    'str': 'some-string',
                    'numeric-str': '123456',
                    'booly-str': '0',
                    'floaty-str': '7.89',
                    'ratio-str': '123:789',
                    'nick-str': 'some-nick',
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': '123456',
                        'sub-dict-booly-str': '0',
                        'sub-dict-floaty-str': '7.89',
                        'sub-dict-ratio-str': '123:789',
                        'sub-dict-nick-str': 'some-nick',
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': '123456',
                            'list-of-dicts-booly-str': '0',
                            'list-of-dicts-floaty-str': '7.89',
                            'list-of-dicts-ratio-str': '123:789',
                            'list-of-dicts-nick-str': 'some-nick',
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': '123456',
                                'list-of-dicts-sub-dict-booly-str': '0',
                                'list-of-dicts-sub-dict-floaty-str': '7.89',
                                'list-of-dicts-sub-dict-ratio-str': '123:789',
                                'list-of-dicts-sub-dict-nick-str': 'some-nick',
                            },
                        }
                    ]
                },
                schema={
                    'str': AttributeSchema(type=str),
                    'numeric-str': AttributeSchema(type=str, is_numeric=True),
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                    'floaty-str': AttributeSchema(type=str, is_floaty=True),
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                    'nick-str': AttributeSchema(type=str, is_nick=True),
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                        'sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'sub-dict-booly-str': AttributeSchema(type=str, is_booly=True),
                        'sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        'sub-dict-nick-str': AttributeSchema(type=str, is_nick=True),
                    },
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'list-of-dicts-str': AttributeSchema(type=str),
                        'list-of-dicts-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'list-of-dicts-booly-str': AttributeSchema(type=str, is_booly=True),
                        'list-of-dicts-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'list-of-dicts-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        'list-of-dicts-nick-str': AttributeSchema(type=str, is_nick=True),
                        'list-of-dicts-sub-dict': {
                            'list-of-dicts-sub-dict-str': AttributeSchema(type=str),
                            'list-of-dicts-sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                            'list-of-dicts-sub-dict-booly-str': AttributeSchema(type=str, is_booly=True),
                            'list-of-dicts-sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                            'list-of-dicts-sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                            'list-of-dicts-sub-dict-nick-str': AttributeSchema(type=str, is_nick=True),
                        },
                    })
                },
                expected={
                    'str': 'some-string',
                    'numeric-str': 123456,
                    'booly-str': False,
                    'floaty-str': 7.89,
                    'ratio-str': 0.16,
                    'nick-str': 'some-nick',
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': 123456,
                        'sub-dict-booly-str': False,
                        'sub-dict-floaty-str': 7.89,
                        'sub-dict-ratio-str': 0.16,
                        'sub-dict-nick-str': 'some-nick',
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': 123456,
                            'list-of-dicts-booly-str': False,
                            'list-of-dicts-floaty-str': 7.89,
                            'list-of-dicts-ratio-str': 0.16,
                            'list-of-dicts-nick-str': 'some-nick',
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': 123456,
                                'list-of-dicts-sub-dict-booly-str': False,
                                'list-of-dicts-sub-dict-floaty-str': 7.89,
                                'list-of-dicts-sub-dict-ratio-str': 0.16,
                                'list-of-dicts-sub-dict-nick-str': 'some-nick',
                            },
                        }
                    ]
                }
            ),
            ParsingTestCase(
                name='handles negative numeric value',
                data={
                    'numeric-str': '-123456',
                },
                schema={
                    'numeric-str': AttributeSchema(type=str, is_numeric=True),
                },
                expected={
                    'numeric-str': -123456,
                }
            ),
            ParsingTestCase(
                name='handles true-ish booly value',
                data={
                    'booly-str': '1',
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                },
                expected={
                    'booly-str': True,
                }
            ),
            ParsingTestCase(
                name='handles false-ish booly value',
                data={
                    'booly-str': '0',
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                },
                expected={
                    'booly-str': False,
                }
            ),
            ParsingTestCase(
                name='handles negative floaty value',
                data={
                    'floaty-str': '-7.89',
                },
                schema={
                    'floaty-str': AttributeSchema(type=str, is_floaty=True),
                },
                expected={
                    'floaty-str': -7.89,
                }
            ),
            ParsingTestCase(
                name='handles zero divisor in ratio',
                data={
                    'ratio-str': '123:0',
                },
                schema={
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                },
                expected={
                    'ratio-str': 123.0,
                }
            ),
            ParsingTestCase(
                name='handles zero ratio',
                data={
                    'ratio-str': '0',
                },
                schema={
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                },
                expected={
                    'ratio-str': 0.0,
                }
            ),
            ParsingTestCase(
                name='applies nick cleaner to nick string',
                data={
                    'str': '[tag] some-string',
                    'nick-str': '[tag] some-nick',
                },
                schema={
                    'str': AttributeSchema(type=str),
                    'nick-str': AttributeSchema(type=str, is_nick=True),
                },
                cleaners={
                    CleanerType.NICK: lambda nick: nick.split(' ').pop()
                },
                expected={
                    'str': '[tag] some-string',
                    'nick-str': 'some-nick',
                }
            )
        ]

        for t in tests:
            # WHEN
            parsed = parse_dict_values(t.data, t.schema, t.cleaners)

            # THEN
            self.assertDictEqual(t.expected, parsed)
