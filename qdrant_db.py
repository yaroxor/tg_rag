import tomllib
from qdrant_client import QdrantClient

with open("secrets.toml", "rb") as f:
    secrets = tomllib.load(f)
    qdrant_url = secrets["qdrant"]["cluster_url"]
    qdrant_api_key = secrets["qdrant"]["api_key"]

qdrant_client = QdrantClient(
    url=qdrant_url, 
    api_key=qdrant_api_key,
)

print(qdrant_client.get_collections())
