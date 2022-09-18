from dataclasses import dataclass
from typing import Dict, Union, Optional


@dataclass
class AttributeSchema:
    type: type
    isnumeric: bool = False
    children: Optional[Dict[str, Union[dict, 'AttributeSchema']]] = None


def is_valid_dict(data: dict, schema: Dict[str, Union[dict, AttributeSchema]]) -> bool:
    return all(is_valid_attribute(data.get(key), attribute_schema) for (key, attribute_schema) in schema.items())


def is_valid_attribute(attribute: Union[str, dict, list], schema: Dict[str, Union[dict, AttributeSchema]]) -> bool:
    if isinstance(schema, AttributeSchema):
        if isinstance(attribute, str) and schema.type == str and schema.isnumeric:
            return attribute.isnumeric()
        if isinstance(attribute, list) and schema.type == list:
            return all(is_valid_attribute(child, schema.children) for child in attribute)
        else:
            return isinstance(attribute, schema.type)
    elif isinstance(attribute, dict) and isinstance(schema, dict):
        return is_valid_dict(attribute, schema)
    else:
        return False
