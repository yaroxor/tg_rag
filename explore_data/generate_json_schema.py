import json

from genson import SchemaBuilder

with open("messages.json", "r") as f:
    chat_history = json.load(f)

builder = SchemaBuilder()

builder.add_object(chat_history)
schema = builder.to_json()

with open("../data/message_schema.json", "w") as f:
    f.write(schema)
