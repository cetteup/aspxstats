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
