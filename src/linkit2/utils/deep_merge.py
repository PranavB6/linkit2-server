from typing import Any


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    """Return the updated result after recursively merging `update` into `base`."""

    result = base.copy()

    for key, update_value in update.items():
        base_value = result.get(key)
        if isinstance(base_value, dict) and isinstance(update_value, dict):
            result[key] = deep_merge(base_value, update_value)  # type: ignore
        else:
            result[key] = update_value
    return result
