from typing import Dict, Union, Tuple, Optional, Any

from .schema import AttributeSchema


def is_valid_dict(
        data: dict,
        schema: Dict[str, Union[dict, AttributeSchema]],
        root: str = ''
) -> Tuple[bool, Optional[str], Optional[Any]]:
    for key, attribute_schema in schema.items():
        valid, path, attribute = is_valid_attribute(join(root, key), data.get(key), attribute_schema)
        if not valid:
            return False, path, attribute
    return True, None, None


def is_valid_attribute(
        path: str,
        attribute: Union[str, dict, list],
        schema: Union[AttributeSchema, Dict[str, AttributeSchema]]
) -> Tuple[bool, Optional[str], Optional[Any]]:
    if isinstance(schema, AttributeSchema):
        if isinstance(attribute, str) and schema.type == str and schema.is_numeric:
            return is_numeric(attribute), path, attribute
        if isinstance(attribute, str) and schema.type == str and schema.is_booly:
            return is_booly(attribute), path, attribute
        if isinstance(attribute, str) and schema.type == str and schema.is_floaty:
            return is_floaty(attribute), path, attribute
        if isinstance(attribute, str) and schema.type == str and schema.is_ratio:
            return is_ratio(attribute), path, attribute
        if isinstance(attribute, list) and schema.type == list:
            for index, child in enumerate(attribute):
                child_valid, child_path, child_attribute = is_valid_attribute(join(path, index), child, schema.children)
                if not child_valid:
                    return False, child_path, child_attribute
            return True, None, None

        return isinstance(attribute, schema.type), path, attribute
    elif isinstance(attribute, dict) and isinstance(schema, dict):
        return is_valid_dict(attribute, schema, root=path)

    return False, path, attribute


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


def join(path: str, key: Union[str, int]) -> str:
    if path == '':
        return key

    return path + '.' + str(key)
