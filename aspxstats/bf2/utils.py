from typing import List, Dict, Union


def group_stats_by_item(
        data: Dict[str, Union[str, int, bool, float]],
        prefix: str,
        keys: List[str]
) -> List[Dict[str, Union[str, int, bool, float]]]:
    """
    Group individual stats attributes by items (weapons, kits, vehicles, maps)
    :param data: dict containing all stats attributes, structured as returned by aspx endpoint
    :param prefix: common prefix of attributes to group
    :param keys: keys of attributes to extract for each item (an id attribute is always extracted)
    :return: list containing a dict with stats for each item
    """
    # Group into dict first, since some entities don't have consecutive ids (e.g. maps use ...,6, 10, 11, 12, 100,...)
    grouped = dict()
    for source_key, value in data.items():
        if not source_key.startswith(prefix):
            continue

        # Format should be "{prefix}{target_key}-{item_id}", e.g. "wtm-0" (weapon time for assault rifles) 
        target_key, _, item_id = source_key[len(prefix):].partition('-')

        if target_key not in keys or not item_id.isnumeric():
            continue

        if item_id not in grouped:
            grouped[item_id] = {
                'id': int(item_id)
            }

        grouped[item_id][target_key] = value

    return list(grouped.values())


def clean_nick(nick: str) -> str:
    return nick.split(' ').pop()

