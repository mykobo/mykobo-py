from typing import Dict


def del_none(d:  Dict):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.
    This alters the input so you may wish to ``copy`` the dict first.
    """

    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

LEDGER_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"