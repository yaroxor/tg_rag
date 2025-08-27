import json
from collections import defaultdict


def to_hashable(value):
    """Convert a value into a hashable form, handling lists and dictionaries."""
    if isinstance(value, dict):
        return tuple(sorted((k, to_hashable(v)) for k, v in value.items()))
    elif isinstance(value, list):
        return tuple(to_hashable(item) for item in value)
    else:
        return value


with open("../data/chat_export.json", "r") as f:
    chat_history = json.load(f)
messages = chat_history["messages"]

explore: defaultdict[ str, set[str] ] = defaultdict(set)

for message in messages:
    for key, value in message.items():
        hashable_value = to_hashable(value)
        explore[key].add(hashable_value)

print(explore)
