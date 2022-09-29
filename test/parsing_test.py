from dataclasses import dataclass
from typing import Dict, Any, Union, List
from unittest import TestCase

from aspxstats.parsing import parse_dict_values
from aspxstats.schema import AttributeSchema


class ParsingTest(TestCase):
    def test_parse(self):
        @dataclass
        class ParsingTestCase:
            name: str
            data: Dict[str, Any]
            schema: Dict[str, Union[AttributeSchema, dict]]
            expected: Dict[str, Any]

        # GIVEN
        tests: List[ParsingTestCase] = [
            ParsingTestCase(
                name='parses complex dict',
                data={
                    'str': 'some-string',
                    'numeric-str': '123456',
                    'floaty-str': '7.89',
                    'ratio-str': '123:789',
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': '123456',
                        'sub-dict-floaty-str': '7.89',
                        'sub-dict-ratio-str': '123:789',
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': '123456',
                            'list-of-dicts-floaty-str': '7.89',
                            'list-of-dicts-ratio-str': '123:789',
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': '123456',
                                'list-of-dicts-sub-dict-floaty-str': '7.89',
                                'list-of-dicts-sub-dict-ratio-str': '123:789',
                            },
                        }
                    ]
                },
                schema={
                    'str': AttributeSchema(type=str),
                    'numeric-str': AttributeSchema(type=str, is_numeric=True),
                    'floaty-str': AttributeSchema(type=str, is_floaty=True),
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                        'sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                    },
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'list-of-dicts-str': AttributeSchema(type=str),
                        'list-of-dicts-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'list-of-dicts-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'list-of-dicts-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        'list-of-dicts-sub-dict': {
                            'list-of-dicts-sub-dict-str': AttributeSchema(type=str),
                            'list-of-dicts-sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                            'list-of-dicts-sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                            'list-of-dicts-sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        },
                    })
                },
                expected={
                    'str': 'some-string',
                    'numeric-str': 123456,
                    'floaty-str': 7.89,
                    'ratio-str': 0.16,
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': 123456,
                        'sub-dict-floaty-str': 7.89,
                        'sub-dict-ratio-str': 0.16,
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': 123456,
                            'list-of-dicts-floaty-str': 7.89,
                            'list-of-dicts-ratio-str': 0.16,
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': 123456,
                                'list-of-dicts-sub-dict-floaty-str': 7.89,
                                'list-of-dicts-sub-dict-ratio-str': 0.16,
                            },
                        }
                    ]
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
            )
        ]

        for t in tests:
            # WHEN
            parsed = parse_dict_values(t.data, t.schema)

            # THEN
            self.assertDictEqual(t.expected, parsed)
