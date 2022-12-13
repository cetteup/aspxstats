from typing import Dict, Union

from .schema import AttributeSchema


def is_valid_dict(data: dict, schema: Dict[str, Union[dict, AttributeSchema]]) -> bool:
    return all(is_valid_attribute(data.get(key), attribute_schema) for (key, attribute_schema) in schema.items())


def is_valid_attribute(attribute: Union[str, dict, list], schema: Dict[str, Union[dict, AttributeSchema]]) -> bool:
    if isinstance(schema, AttributeSchema):
        if isinstance(attribute, str) and schema.type == str and schema.is_numeric:
            return is_numeric(attribute)
        if isinstance(attribute, str) and schema.type == str and schema.is_booly:
            return is_booly(attribute)
        if isinstance(attribute, str) and schema.type == str and schema.is_floaty:
            return is_floaty(attribute)
        if isinstance(attribute, str) and schema.type == str and schema.is_ratio:
            return is_ratio(attribute)
        if isinstance(attribute, list) and schema.type == list:
            return all(is_valid_attribute(child, schema.children) for child in attribute)
        else:
            return isinstance(attribute, schema.type)
    elif isinstance(attribute, dict) and isinstance(schema, dict):
        return is_valid_dict(attribute, schema)
    else:
        return False


def is_numeric(value: str) -> bool:
    """
    Test whether a string is parseable to int
    (used instead of str.isnumeric(), since that cannot handle negative numbers)
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_booly(value: str) -> bool:
    """
    Test whether a string is a parseable as a boolean-like integer (0 or 1)
    """
    try:
        parsed = int(value)
        return 0 <= parsed <= 1
    except ValueError:
        return False


def is_floaty(value: str) -> bool:
    """
    Test whether a string is parseable to float
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_ratio(value: str) -> bool:
    """
    Test whether a string is ratio of two integers ("123:789", with "0" being accepted as the zero value)
    """
    elements = value.split(':', 1)
    return len(elements) == 2 and all(is_numeric(elem) for elem in elements) or value == '0'
