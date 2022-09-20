from typing import Dict, Union

from aspxstats.validation import AttributeSchema

SEARCHFORPLAYERS_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'asof': AttributeSchema(type=str, isnumeric=True),
    'results': AttributeSchema(type=list, children={
        'n': AttributeSchema(type=str, isnumeric=True),
        'pid': AttributeSchema(type=str, isnumeric=True),
        'nick': AttributeSchema(type=str),
        'score': AttributeSchema(type=str, isnumeric=True)
    })
}

GETLEADERBOARD_RESPONSE_SCHEMA: Dict[str, Union[dict, AttributeSchema]] = {
    'size': AttributeSchema(type=str, isnumeric=True),
    'asof': AttributeSchema(type=str, isnumeric=True),
    'entries': AttributeSchema(type=list, children={
        'n': AttributeSchema(type=str, isnumeric=True),
        'pid': AttributeSchema(type=str, isnumeric=True),
        'nick': AttributeSchema(type=str),
        'playerrank': AttributeSchema(type=str, isnumeric=True),
        'countrycode': AttributeSchema(type=str)
    })
}
