from typing import Union, Dict, List, Callable, Optional

from .schema import AttributeSchema
from .types import CleanerType


def parse_dict_values(
        data: dict,
        schema: Dict[str, Union[dict, AttributeSchema]],
        cleaners: Optional[Dict[CleanerType, Callable[[str], str]]] = None
) -> dict:
    """
    Parses all schema-referenced values in dict to their desired type.
    Assumes that ``is_valid_dict`` successfully validated the ``data`` dict.
    Omits any values found in ``data`` that are not referenced in ``schema``.

    :param data: dict containing values to be parsed
    :param schema: :class:`AttributeSchema` defining the structure of the dict and the desired type for its values
    :param cleaners: dict of cleaner functions used to clean the values before parsing
    :return: dict containing correctly types values
    """
    parsed = dict()
    for key, value_schema in schema.items():
        parsed[key] = parse_dict_value(data[key], value_schema, cleaners)

    return parsed


def parse_dict_value(
        value: Union[str, dict, list],
        schema: Dict[str, Union[dict, AttributeSchema]],
        cleaners: Optional[Dict[CleanerType, Callable[[str], str]]] = None
) -> Union[str, int, float, Dict[str, Union[str, int, float]], List[Dict[str, Union[str, int, float]]]]:
    if isinstance(schema, AttributeSchema):
        if schema.is_numeric:
            return int(value)
        if schema.is_booly:
            return int(value) == 1
        if schema.is_floaty:
            return float(value)
        if schema.is_ratio:
            if value == '0':
                return 0.0
            dividend, divisor = [int(e) for e in value.split(':', 1)]
            # Cast dividend to float to return a consistent type in both cases
            return round(dividend / divisor, 2) if divisor > 0 else float(dividend)
        if schema.is_nick and cleaners is not None and callable(cleaners.get(CleanerType.NICK)):
            return cleaners[CleanerType.NICK](value)
        if schema.type == list:
            return [parse_dict_values(child, schema.children, cleaners) for child in value]
        else:
            return value
    else:
        return parse_dict_values(value, schema, cleaners)
