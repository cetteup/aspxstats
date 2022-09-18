from dataclasses import dataclass
from typing import Dict, Union, List, Any
from unittest import TestCase

from aspxstats.validation import AttributeSchema, is_valid_dict


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
                    'sub-dict': {
                        'sub-dict-str': 'some-string',
                        'sub-dict-numeric-str': '123456',
                    },
                    'list-of-dicts': [
                        {
                            'list-of-dicts-str': 'some-string',
                            'list-of-dicts-numeric-str': '123456',
                            'list-of-dicts-sub-dict': {
                                'list-of-dicts-sub-dict-str': 'some-string',
                                'list-of-dicts-sub-dict-numeric-str': '123456',
                            },
                        }
                    ]
                },
                schema={
                    'str': AttributeSchema(type=str),
                    'numeric-str': AttributeSchema(type=str, isnumeric=True),
                    'sub-dict': {
                        'sub-dict-str': AttributeSchema(type=str),
                        'sub-dict-numeric-str': AttributeSchema(type=str, isnumeric=True)
                    },
                    'list-of-dicts': AttributeSchema(type=list, children={
                        'list-of-dicts-str': AttributeSchema(type=str),
                        'list-of-dicts-numeric-str': AttributeSchema(type=str, isnumeric=True),
                        'list-of-dicts-sub-dict': {
                            'list-of-dicts-sub-dict-str': AttributeSchema(type=str),
                            'list-of-dicts-sub-dict-numeric-str': AttributeSchema(type=str, isnumeric=True)
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
                    'numeric-str': AttributeSchema(type=str, isnumeric=True),
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
                        'sub-dict-numeric-str': AttributeSchema(type=str, isnumeric=True),
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
                        'numeric-str': AttributeSchema(type=str, isnumeric=True),
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
