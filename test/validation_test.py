from dataclasses import dataclass
from typing import Dict, Union, List, Any
from unittest import TestCase

from aspxstats.validation import is_valid_dict
from aspxstats.schema import AttributeSchema


class ValidationTest(TestCase):
    def test_validate(self):
        @dataclass
        class ValidationTestCase:
            name: str
            data: Dict[str, Any]
            schema: Dict[str, Union[AttributeSchema, dict]]
            wantIsValid: bool

        # GIVEN
        tests: List[ValidationTestCase] = [
            ValidationTestCase(
                name='true for data matching schema',
                data={
                    'str': 'some-string',
                    'numeric-str': '123456',
                    'booly-str': '0',
                    'floaty-str': '7.89',
                    'ratio-str': '123:789',
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': '123456',
                        'sub-dict-booly-str': '0',
                        'sub-dict-floaty-str': '7.89',
                        'sub-dict-ratio-str': '123:789',
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': '123456',
                            'list-of-dicts-booly-str': '0',
                            'list-of-dicts-floaty-str': '7.89',
                            'list-of-dicts-ratio-str': '123:789',
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': '123456',
                                'list-of-dicts-sub-dict-booly-str': '0',
                                'list-of-dicts-sub-dict-floaty-str': '7.89',
                                'list-of-dicts-sub-dict-ratio-str': '123:789',
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
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                        'sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'sub-dict-booly-str': AttributeSchema(type=str, is_booly=True),
                        'sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                    },
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'list-of-dicts-str': AttributeSchema(type=str),
                        'list-of-dicts-numeric-str': AttributeSchema(type=str, is_numeric=True),
                        'list-of-dicts-booly-str': AttributeSchema(type=str, is_booly=True),
                        'list-of-dicts-floaty-str': AttributeSchema(type=str, is_floaty=True),
                        'list-of-dicts-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        'list-of-dicts-sub-dict': {
                            'list-of-dicts-sub-dict-str': AttributeSchema(type=str),
                            'list-of-dicts-sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                            'list-of-dicts-sub-dict-booly-str': AttributeSchema(type=str, is_booly=True),
                            'list-of-dicts-sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                            'list-of-dicts-sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                        },
                    })
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for data matching schema with additional attributes',
                data={
                    'str': '123456',
                    'additional-key': 'some-value'
                },
                schema={
                    'str': AttributeSchema(type=str),
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for negative numeric-string',
                data={
                    'numeric-str': '-1'
                },
                schema={
                    'numeric-str': AttributeSchema(type=str, is_numeric=True)
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for true-ish booly-string',
                data={
                    'booly-str': '1'
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True)
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for false-ish booly-string',
                data={
                    'booly-str': '0'
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True)
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for negative floaty-string',
                data={
                    'numeric-str': '-1.0'
                },
                schema={
                    'numeric-str': AttributeSchema(type=str, is_floaty=True)
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='true for zero value ratio-string string attribute',
                data={
                    'ratio-str': '0',
                },
                schema={
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                },
                wantIsValid=True
            ),
            ValidationTestCase(
                name='false for non-string string attribute',
                data={
                    'str': 123456,
                },
                schema={
                    'str': AttributeSchema(type=str),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-numeric-string string attribute',
                data={
                    'numeric-str': 'not-a-numeric-string',
                },
                schema={
                    'numeric-str': AttributeSchema(type=str, is_numeric=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-numeric non-booly-string string attribute',
                data={
                    'booly-str': 'not-a-numeric-string',
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for negative non-booly-string string attribute',
                data={
                    'booly-str': '-1',
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for positive non-booly-string string attribute',
                data={
                    'booly-str': '2',
                },
                schema={
                    'booly-str': AttributeSchema(type=str, is_booly=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-floaty-string string attribute',
                data={
                    'floaty-str': 'not-a-floaty-string',
                },
                schema={
                    'floaty-str': AttributeSchema(type=str, is_floaty=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-ratio-string string attribute',
                data={
                    'ratio-str': 'not-a-ratio-string',
                },
                schema={
                    'ratio-str': AttributeSchema(type=str, is_ratio=True),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for missing attribute',
                data={
                    'some-other-key': 'some-value',
                },
                schema={
                    'str': AttributeSchema(type=str),
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-string string attribute in sub-dict attribute',
                data={
                    'sub-dict': {
                        'sub-dict-str': 123456,
                    },
                },
                schema={
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-numeric-string string attribute in sub-dict attribute',
                data={
                    'sub-dict': {
                        'sub-dict-numeric-str': 'not-a-numeric-string',
                    },
                },
                schema={
                    'sub-dict': {
                        'sub-dict-numeric-str': AttributeSchema(type=str, is_numeric=True),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-floaty-string string attribute in sub-dict attribute',
                data={
                    'sub-dict': {
                        'sub-dict-floaty-str': 'not-a-floaty-string',
                    },
                },
                schema={
                    'sub-dict': {
                        'sub-dict-floaty-str': AttributeSchema(type=str, is_floaty=True),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-ratio-string string attribute in sub-dict attribute',
                data={
                    'sub-dict': {
                        'sub-dict-ratioo-str': 'not-a-ratio-string',
                    },
                },
                schema={
                    'sub-dict': {
                        'sub-dict-ratio-str': AttributeSchema(type=str, is_ratio=True),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for missing attribute in sub-dict attribute',
                data={
                    'sub-dict': {
                        'some-other-key': 'some-value',
                    },
                },
                schema={
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-dict sub-dict attribute',
                data={
                    'sub-dict': 'not-a-dict'
                },
                schema={
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                    },
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-string child attribute in list attribute',
                data={
                    'list-of-dicts': [
                        {
                            'str': 123456,
                        }
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'str': AttributeSchema(type=str),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-numeric-string child attribute in list attribute',
                data={
                    'list-of-dicts': [
                        {
                            'numeric-str': 'not-a-numeric-string',
                        }
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'numeric-str': AttributeSchema(type=str, is_numeric=True),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-floaty-string child attribute in list attribute',
                data={
                    'list-of-dicts': [
                        {
                            'floaty-str': 'not-a-floaty-string',
                        }
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'floaty-str': AttributeSchema(type=str, is_floaty=True),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-ratio-string child attribute in list attribute',
                data={
                    'list-of-dicts': [
                        {
                            'ratio-str': 'not-a-ratio-string',
                        }
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'ratio-str': AttributeSchema(type=str, is_floaty=True),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for missing child attribute in list attribute',
                data={
                    'list-of-dicts': [
                        {
                            'some-other-key': 'some-value',
                        }
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'str': AttributeSchema(type=str),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false for non-dict child in list attribute',
                data={
                    'list-of-dicts': [
                        'not-a-dict'
                    ],
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'str': AttributeSchema(type=str),
                    })
                },
                wantIsValid=False
            ),
            ValidationTestCase(
                name='false non-list list attribute',
                data={
                    'list-of-dicts': 'not-a-list',
                },
                schema={
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'str': AttributeSchema(type=str),
                    })
                },
                wantIsValid=False
            ),
        ]

        for t in tests:
            # WHEN
            valid = is_valid_dict(t.data, t.schema)

            # THEN
            self.assertEqual(t.wantIsValid, valid, f'"{t.name}" failed\nexpected: {t.wantIsValid}\nactual: {valid}')
